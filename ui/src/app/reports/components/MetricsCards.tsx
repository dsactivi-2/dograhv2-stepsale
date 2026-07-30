import { Phone,PhoneForwarded } from 'lucide-react';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface MetricsCardsProps {
  metrics: {
    total_runs: number;
    xfer_count: number;
    success_count?: number;
  };
}

export function MetricsCards({ metrics }: MetricsCardsProps) {
  const successCount = metrics.success_count ?? metrics.xfer_count;
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Total Workflow Runs</CardTitle>
          <Phone className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{metrics.total_runs.toLocaleString()}</div>
          <p className="text-xs text-muted-foreground">
            Total calls processed today
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Success Dispositions</CardTitle>
          <PhoneForwarded className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{successCount.toLocaleString()}</div>
          <p className="text-xs text-muted-foreground">
            Matches workflow success_codes (fallback: XFER)
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
