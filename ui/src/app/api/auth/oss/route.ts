/*
  Provides authentication token to LocalProviderWrapper once loaded
  in the browser.
  Returns 401 if no token cookie exists (user needs to log in).

  Enriches is_superuser from the backend so the UI reflects DB state even
  if the session cookie was set before that field existed on login.
*/
import { cookies } from 'next/headers';
import { NextResponse } from 'next/server';

import { getServerBackendUrl } from '@/lib/apiClient';
import { getAuthProvider } from '@/lib/auth/config';

const OSS_TOKEN_COOKIE = 'dograh_auth_token';
const OSS_USER_COOKIE = 'dograh_auth_user';

export async function GET() {
  const authProvider = await getAuthProvider();

  // Only handle OSS mode
  if (authProvider !== 'local') {
    return NextResponse.json({ error: 'Not in OSS mode' }, { status: 400 });
  }

  const cookieStore = await cookies();
  const token = cookieStore.get(OSS_TOKEN_COOKIE)?.value;
  const userRaw = cookieStore.get(OSS_USER_COOKIE)?.value;

  // If no token exists, return 401 (user needs to sign up or log in)
  if (!token) {
    return NextResponse.json({ error: 'Not authenticated' }, { status: 401 });
  }

  let user: Record<string, unknown> = userRaw
    ? JSON.parse(userRaw)
    : { id: token, name: 'Local User', provider: 'local' };

  // Always attach provider for LocalUser typing
  user = { ...user, provider: user.provider ?? 'local' };

  // Live-enrich superuser from API (source of truth = DB)
  try {
    const backendUrl = getServerBackendUrl();
    const res = await fetch(`${backendUrl}/api/v1/user/auth/user`, {
      headers: { Authorization: `Bearer ${token}` },
      cache: 'no-store',
    });
    if (res.ok) {
      const authUser = (await res.json()) as { id?: number; is_superuser?: boolean };
      user = {
        ...user,
        id: authUser.id ?? user.id,
        is_superuser: Boolean(authUser.is_superuser),
      };
    }
  } catch {
    // keep cookie user if backend enrichment fails
  }

  return NextResponse.json({
    token,
    user,
  });
}
