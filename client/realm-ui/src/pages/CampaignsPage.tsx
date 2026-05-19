import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Badge, Card } from "../components/ui";
import type { Campaign } from "../types";
import styles from "./CampaignsPage.module.css";

// Placeholder data — replace with getCampaigns() from api/client.ts
const MOCK_CAMPAIGNS: Campaign[] = [
  {
    campaign_id: "11111111-0000-0000-0000-000000000001",
    title: "Curse of Strahd",
    description: "A gothic horror adventure in the mist-shrouded land of Barovia.",
    status: "active",
    dm_username: "Alex",
    player_count: 4,
    max_players: 5,
    session_count: 7,
  },
  {
    campaign_id: "11111111-0000-0000-0000-000000000002",
    title: "Descent into Avernus",
    description: "Hell's armies mass on the surface. Only you can stop the Blood War.",
    status: "recruiting",
    dm_username: "Jordan",
    player_count: 3,
    max_players: 5,
    session_count: 2,
  },
  {
    campaign_id: "11111111-0000-0000-0000-000000000003",
    title: "Ghosts of Saltmarsh",
    description: "Nautical intrigue on the Sword Coast — sea monsters, pirates, and politics.",
    status: "paused",
    dm_username: "Sam",
    player_count: 5,
    max_players: 5,
    session_count: 14,
  },
];

const STATUS_BADGE: Record<Campaign["status"], "success" | "gold" | "warning"> = {
  active: "success",
  recruiting: "gold",
  paused: "warning",
};

const CAMPAIGN_ICONS: Record<string, string> = {
  "Curse of Strahd": "⛰",
  "Descent into Avernus": "🔥",
  "Ghosts of Saltmarsh": "⚓",
};

export function CampaignsPage() {
  const navigate = useNavigate();

  // TODO: replace mock with:
  // const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  // useEffect(() => { getCampaigns().then(r => setCampaigns(r.campaign_data)); }, []);
  const [campaigns] = useState<Campaign[]>(MOCK_CAMPAIGNS);

  const active    = campaigns.filter((c) => c.status === "active").length;
  const sessions  = campaigns.reduce((sum, c) => sum + c.session_count, 0);

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>My Campaigns</h1>
          <p className={styles.subtitle}>
            {active} active · {campaigns.length} total
          </p>
        </div>
        <div className={styles.headerActions}>
          <Button variant="ghost" size="sm" onClick={() => navigate("/campaigns/join")}>
            Join campaign
          </Button>
          {/* TODO: wire up to POST /v1/campaigns/create */}
          <Button variant="primary" size="sm">
            + New campaign
          </Button>
        </div>
      </div>

      {/* Summary stats */}
      <div className={styles.statsRow}>
        {[
          { label: "Active", value: active },
          { label: "Campaigns", value: campaigns.length },
          { label: "Sessions played", value: sessions },
        ].map((stat) => (
          <div key={stat.label} className={styles.statCard}>
            <span className={styles.statValue}>{stat.value}</span>
            <span className={styles.statLabel}>{stat.label}</span>
          </div>
        ))}
      </div>

      {/* Campaign list */}
      <div className={styles.list}>
        {campaigns.map((campaign) => (
          <Card
            key={campaign.campaign_id}
            hoverable
            className={styles.campaignCard}
            onClick={() => navigate(`/campaigns/${campaign.campaign_id}`)}
          >
            <div className={styles.campaignCardInner}>
              <div className={styles.campaignIcon} aria-hidden="true">
                {CAMPAIGN_ICONS[campaign.title] ?? "⚔"}
              </div>

              <div className={styles.campaignInfo}>
                <div className={styles.campaignTitleRow}>
                  <h2 className={styles.campaignTitle}>{campaign.title}</h2>
                  <Badge variant={STATUS_BADGE[campaign.status]}>
                    {campaign.status}
                  </Badge>
                </div>
                <p className={styles.campaignMeta}>
                  DM: {campaign.dm_username} · {campaign.player_count}/{campaign.max_players} players · Session {campaign.session_count}
                </p>
                <p className={styles.campaignDesc}>{campaign.description}</p>
              </div>

              <span className={styles.chevron} aria-hidden="true">›</span>
            </div>
          </Card>
        ))}

        {campaigns.length === 0 && (
          <div className={styles.empty}>
            <p className={styles.emptyIcon}>🗺</p>
            <p className={styles.emptyText}>No campaigns yet.</p>
            <Button
              variant="primary"
              size="md"
              onClick={() => navigate("/campaigns/join")}
            >
              Join your first campaign
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
