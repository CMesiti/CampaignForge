import { useState } from "react";
import { Button, Input, Badge, Card } from "../components/ui";
import styles from "./JoinCampaignPage.module.css";

export function JoinCampaignPage() {
  const [campaignId, setCampaignId] = useState("");
  const [previewing, setPreviewing] = useState(false);
  const [joining, setJoining] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [joined, setJoined] = useState(false);

  async function handleLookup(e: React.FormEvent) {
    e.preventDefault();
    if (!campaignId.trim()) return;
    setError(null);
    setPreviewing(true);
    // TODO: you may want a GET /v1/campaigns/:campaign_id endpoint for previewing
    // For now we just show a mock preview after validation
  }

  async function handleJoin() {
    setJoining(true);
    setError(null);
    try {
      // TODO: call joinCampaign(campaignId) from api/client.ts
      // await joinCampaign(campaignId);
      await new Promise((r) => setTimeout(r, 900));
      setJoined(true);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Could not join campaign");
    } finally {
      setJoining(false);
    }
  }

  if (joined) {
    return (
      <div className={styles.successPage}>
        <span className={styles.successRune}>⚔</span>
        <h2 className={styles.successTitle}>You've joined the campaign</h2>
        <p className={styles.successSub}>Head to the campaign page to create your character.</p>
        {/* TODO: navigate to /campaigns/:campaignId */}
        <Button variant="primary" size="lg">Go to campaign</Button>
      </div>
    );
  }

  return (
    <div className={styles.page}>
      <div className={styles.inner}>
        <h1 className={styles.title}>Join a Campaign</h1>
        <p className={styles.subtitle}>Enter the campaign ID shared by your Dungeon Master.</p>

        <form className={styles.lookupForm} onSubmit={handleLookup} noValidate>
          <Input
            label="Campaign ID"
            name="campaign_id"
            type="text"
            placeholder="e.g. 550e8400-e29b-41d4-a716-446655440000"
            value={campaignId}
            onChange={(e) => {
              setCampaignId(e.target.value);
              setPreviewing(false);
              setError(null);
            }}
            hint="Paste the UUID your DM sent you"
          />
          <Button type="submit" variant="primary" size="md">
            Look up campaign
          </Button>
        </form>

        {error && <p className={styles.errorMsg}>{error}</p>}

        {/* Preview card — shown after lookup */}
        {previewing && (
          <Card className={styles.previewCard}>
            <div className={styles.previewHeader}>
              <div className={styles.previewIcon} aria-hidden="true">⛰</div>
              <div>
                <h2 className={styles.previewTitle}>Curse of Strahd</h2>
                <p className={styles.previewMeta}>DM: Alex · 3/5 players · Level 3 start</p>
              </div>
            </div>

            <p className={styles.previewDesc}>
              A gothic horror adventure set in the mist-shrouded land of Barovia. Face the vampire
              lord Strahd and uncover the dark secrets of this cursed realm.
            </p>

            <div className={styles.previewTags}>
              <Badge variant="gold">Gothic horror</Badge>
              <Badge variant="warning">Level 3 start</Badge>
              <Badge variant="success">Open slot</Badge>
            </div>

            <div className={styles.previewDivider} />

            <Button
              variant="primary"
              size="lg"
              loading={joining}
              onClick={handleJoin}
              className={styles.joinBtn}
            >
              Join campaign
            </Button>
          </Card>
        )}
      </div>
    </div>
  );
}
