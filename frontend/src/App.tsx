import { Navigate, Route, Routes } from 'react-router-dom';
import { AppLayout } from './layouts/AppLayout';
import { DashboardPage } from './pages/DashboardPage';
import { LoginPage } from './pages/LoginPage';
import { MixBuilderPage } from './pages/MixBuilderPage';
import { ProjectDetailPage } from './pages/ProjectDetailPage';
import { ProjectsPage } from './pages/ProjectsPage';
import { ReportsPage } from './pages/ReportsPage';
import { ResultsPage } from './pages/ResultsPage';
import { ScenariosPage } from './pages/ScenariosPage';
import { VariantEditorPage } from './pages/VariantEditorPage';

function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/projects" element={<ProjectsPage />} />
        <Route path="/projects/:id" element={<ProjectDetailPage />} />
        <Route path="/variant-editor" element={<VariantEditorPage />} />
        <Route path="/mix-builder" element={<MixBuilderPage />} />
        <Route path="/scenarios" element={<ScenariosPage />} />
        <Route path="/results" element={<ResultsPage />} />
        <Route path="/reports" element={<ReportsPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}

export default App;
