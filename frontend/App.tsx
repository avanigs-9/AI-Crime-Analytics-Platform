import { useCallback, useEffect, useState } from 'react';
import { AuthProvider, useAuth } from '@/context/AuthContext';
import { Layout, type PageId } from '@/components/Layout';
import { LoginPage } from '@/pages/LoginPage';
import { Dashboard } from '@/pages/Dashboard';
import { Analytics } from '@/pages/Analytics';
import { Hotspots } from '@/pages/Hotspots';
import { CsvUpload } from '@/pages/CsvUpload';
import { Prediction } from '@/pages/Prediction';
import { Records } from '@/pages/Records';
import { fetchCrimeRecords } from '@/lib/api';
import type { CrimeRecord } from '@/types';
import { Loader2 } from 'lucide-react';

function AppContent() {
  const { session, loading } = useAuth();
  const [page, setPage] = useState<PageId>('dashboard');
  const [records, setRecords] = useState<CrimeRecord[]>([]);
  const [recordsLoading, setRecordsLoading] = useState(true);

  const loadRecords = useCallback(async () => {
    setRecordsLoading(true);
    try {
      const data = await fetchCrimeRecords();
      setRecords(data);
    } catch (err) {
      console.error('Failed to load records:', err);
    } finally {
      setRecordsLoading(false);
    }
  }, []);

  useEffect(() => {
    if (session) loadRecords();
  }, [session, loadRecords]);

  if (loading) {
    return (
      <div className="min-h-screen bg-navy-950 flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-accent-400 animate-spin" />
      </div>
    );
  }

  if (!session) {
    return <LoginPage />;
  }

  return (
    <Layout currentPage={page} onNavigate={setPage}>
      {page === 'dashboard' && <Dashboard records={records} loading={recordsLoading} onNavigate={setPage} />}
      {page === 'analytics' && <Analytics records={records} loading={recordsLoading} />}
      {page === 'hotspots' && <Hotspots records={records} loading={recordsLoading} />}
      {page === 'upload' && <CsvUpload onUploaded={loadRecords} />}
      {page === 'prediction' && <Prediction records={records} />}
      {page === 'records' && <Records records={records} loading={recordsLoading} />}
    </Layout>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
