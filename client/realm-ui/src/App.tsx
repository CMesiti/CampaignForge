import { BrowserRouter, Routes, Route, Navigate, Outlet } from "react-router-dom";
import { AppShell } from "./components/layout/AppShell";
import { AuthPage } from "./pages/AuthPage";
import { CampaignsPage } from "./pages/CampaignsPage";
import { JoinCampaignPage } from "./pages/JoinCampaignPage";
import { CampaignDetailPage } from "./pages/CampaignDetailPage";
import { CharacterCreationPage } from "./pages/CharacterCreationPage";

// Layout wrapper — AppShell renders nav + <Outlet> for child routes
function ShellLayout() {
  return (
    <AppShell>
      <Outlet />
    </AppShell>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public */}
        <Route path="/login" element={<AuthPage />} />

        {/* Root redirect */}
        <Route index element={<Navigate to="/campaigns" replace />} />

        {/* Protected — all share the AppShell layout */}
        <Route element={<ShellLayout />}>
          <Route path="/campaigns" element={<CampaignsPage />} />
          <Route path="/campaigns/join" element={<JoinCampaignPage />} />
          <Route path="/campaigns/:campaignId" element={<CampaignDetailPage />} />
          <Route path="/campaigns/:campaignId/character/new" element={<CharacterCreationPage />} />
        </Route>

        {/* Catch-all */}
        <Route path="*" element={<Navigate to="/campaigns" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
