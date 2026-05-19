import { useState, useRef, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Button, Avatar, Badge, Card } from "../components/ui";
import type { PlayerCharacter, ChatMessage } from "../types";
import styles from "./CampaignDetailPage.module.css";

// ─── Mock data — replace with getPlayerCharacters(campaignId) ───────────────
const MOCK_MEMBERS: PlayerCharacter[] = [
  {
    character_id: "c1", campaign_id: "", user_id: "",
    player_name: "Alex", character_name: "", race: "", char_class: "",
    background: "", alignment: "", level: 0,
    ability_scores: { strength:0,dexterity:0,constitution:0,intelligence:0,wisdom:0,charisma:0 },
  },
  {
    character_id: "c2", campaign_id: "", user_id: "",
    player_name: "Sam R.", character_name: "Arannis Moonwhisper",
    race: "Wood Elf", char_class: "Ranger", background: "Outlander",
    alignment: "Neutral Good", level: 5,
    ability_scores: { strength:10,dexterity:16,constitution:14,intelligence:12,wisdom:13,charisma:8 },
  },
  {
    character_id: "c3", campaign_id: "", user_id: "",
    player_name: "Jordan D.", character_name: "Brom Stonefist",
    race: "Dwarf", char_class: "Fighter", background: "Soldier",
    alignment: "Lawful Good", level: 5,
    ability_scores: { strength:18,dexterity:10,constitution:16,intelligence:9,wisdom:12,charisma:8 },
  },
  {
    character_id: "c4", campaign_id: "", user_id: "",
    player_name: "Maya K.", character_name: "Seraphina",
    race: "Human", char_class: "Cleric", background: "Acolyte",
    alignment: "Lawful Good", level: 5,
    ability_scores: { strength:10,dexterity:12,constitution:13,intelligence:14,wisdom:17,charisma:13 },
  },
];

const AVATAR_COLORS = ["purple", "teal", "coral", "amber", "blue"] as const;

type Tab = "members" | "chat" | "notes";

export function CampaignDetailPage() {
  const { campaignId } = useParams<{ campaignId: string }>();
  const [activeTab, setActiveTab] = useState<Tab>("members");
  const [members] = useState<PlayerCharacter[]>(MOCK_MEMBERS);

  return (
    <div className={styles.page}>
      <div className={styles.pageHeader}>
        <div>
          <h1 className={styles.title}>Curse of Strahd</h1>
          <p className={styles.meta}>Session 7 · {members.length} players · DM: Alex</p>
        </div>
        <Badge variant="success">Active</Badge>
      </div>

      {/* Tabs */}
      <div className={styles.tabs}>
        {(["members", "chat", "notes"] as Tab[]).map((t) => (
          <button
            key={t}
            className={`${styles.tab} ${activeTab === t ? styles["tab--active"] : ""}`}
            onClick={() => setActiveTab(t)}
            type="button"
          >
            {t === "chat" ? "Rules chat" : t.charAt(0).toUpperCase() + t.slice(1)}
          </button>
        ))}
      </div>

      <div className={styles.tabContent}>
        {activeTab === "members" && (
          <MembersTab members={members} campaignId={campaignId!} />
        )}
        {activeTab === "chat" && (
          <ChatTab campaignId={campaignId!} />
        )}
        {activeTab === "notes" && (
          <NotesTab />
        )}
      </div>
    </div>
  );
}

// ─── Members Tab ─────────────────────────────────────────────────────────────

function MembersTab({ members, campaignId }: { members: PlayerCharacter[]; campaignId: string }) {
  return (
    <div className={styles.membersTab}>
      <div className={styles.memberList}>
        {/* DM row — first member has no character */}
        {members.map((m, i) => {
          const isDM = i === 0;
          const color = AVATAR_COLORS[i % AVATAR_COLORS.length];
          const initials = m.player_name.split(" ").map((n) => n[0]).join("").slice(0, 2);

          return (
            <div key={m.character_id} className={styles.memberRow}>
              <Avatar initials={initials} size="md" color={color} />
              <div className={styles.memberInfo}>
                <span className={styles.memberName}>{m.player_name}</span>
                {m.character_name && (
                  <span className={styles.memberChar}>
                    — {m.character_name} · {m.race} {m.char_class} · Lv {m.level}
                  </span>
                )}
                {!m.character_name && !isDM && (
                  <span className={styles.memberNoChar}>No character yet</span>
                )}
              </div>
              {isDM && <Badge variant="gold">DM</Badge>}
              {!isDM && m.character_name && (
                <Button variant="ghost" size="sm">View sheet</Button>
              )}
              {!isDM && !m.character_name && (
                /* TODO: navigate to /campaigns/:campaignId/character/new */
                <Button variant="primary" size="sm">Create character</Button>
              )}
            </div>
          );
        })}

        {/* Open slot placeholder */}
        <div className={`${styles.memberRow} ${styles["memberRow--open"]}`}>
          <div className={styles.openSlot} aria-hidden="true">+</div>
          <span className={styles.openSlotLabel}>Open slot</span>
          <Badge variant="neutral">1 / 5</Badge>
        </div>
      </div>

      <div className={styles.memberActions}>
        {/* TODO: wire to DELETE /v1/campaigns/:campaignId/:userId */}
        <Button variant="danger" size="sm">Leave campaign</Button>
      </div>
    </div>
  );
}

// ─── Chat Tab ─────────────────────────────────────────────────────────────────

function ChatTab({ campaignId }: { campaignId: string }) {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content: "I'm your 5e rules assistant. Ask me anything about D&D rules, spells, conditions, or mechanics — I'll pull the answer straight from the rulebook.",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [streaming, setStreaming] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend(e: React.FormEvent) {
    e.preventDefault();
    const query = input.trim();
    if (!query || streaming) return;

    setInput("");
    setMessages((prev) => [
      ...prev,
      { role: "user", content: query, timestamp: new Date() },
    ]);
    setStreaming(true);

    // Add empty assistant message for streaming to fill
    setMessages((prev) => [
      ...prev,
      { role: "assistant", content: "", timestamp: new Date() },
    ]);

    try {
      // TODO: wire up to queryAgent() from api/client.ts
      // await queryAgent(campaignId, { user_query: query }, (chunk) => {
      //   setMessages((prev) => {
      //     const updated = [...prev];
      //     updated[updated.length - 1] = {
      //       ...updated[updated.length - 1],
      //       content: updated[updated.length - 1].content + chunk,
      //     };
      //     return updated;
      //   });
      // });

      // Placeholder streaming simulation
      const placeholder = "According to the Player's Handbook, grappling works by making a Strength (Athletics) check contested by the target's Strength (Athletics) or Dexterity (Acrobatics). The target can be no more than one size larger than you.";
      for (const char of placeholder) {
        await new Promise((r) => setTimeout(r, 18));
        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = {
            ...updated[updated.length - 1],
            content: updated[updated.length - 1].content + char,
          };
          return updated;
        });
      }
    } finally {
      setStreaming(false);
    }
  }

  return (
    <div className={styles.chatTab}>
      <div className={styles.chatMessages}>
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`${styles.chatBubble} ${
              msg.role === "user" ? styles["chatBubble--user"] : styles["chatBubble--ai"]
            }`}
          >
            {msg.role === "assistant" && (
              <span className={styles.chatSource}>5e Rulebook · RAG</span>
            )}
            <p className={styles.chatContent}>
              {msg.content}
              {msg.role === "assistant" && streaming && i === messages.length - 1 && (
                <span className={styles.cursor} aria-hidden="true" />
              )}
            </p>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <form className={styles.chatForm} onSubmit={handleSend}>
        <input
          className={styles.chatInput}
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a 5e rules question…"
          disabled={streaming}
        />
        <Button
          type="submit"
          variant="primary"
          size="sm"
          loading={streaming}
          disabled={!input.trim()}
        >
          ↑
        </Button>
      </form>
    </div>
  );
}

// ─── Notes Tab ───────────────────────────────────────────────────────────────

function NotesTab() {
  return (
    <Card className={styles.notesTab}>
      <p className={styles.notesMeta}>Session notes — coming soon</p>
      <textarea
        className={styles.notesArea}
        placeholder="Keep track of important plot points, NPC names, or quest hooks…"
        rows={10}
      />
      <Button variant="primary" size="sm" className={styles.notesSave}>Save notes</Button>
    </Card>
  );
}
