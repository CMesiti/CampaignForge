import { useState } from "react";
import { useParams } from "react-router-dom";
import { Button, Input, Select, Textarea, StatBox, StepProgress } from "../components/ui";
import type { AbilityScores } from "../types";
import styles from "./CharacterCreationPage.module.css";

const STEPS = ["Identity", "Race & Class", "Abilities", "Backstory"];

const RACE_OPTIONS = [
  { value: "human", label: "Human" },
  { value: "elf_high", label: "High Elf" },
  { value: "elf_wood", label: "Wood Elf" },
  { value: "dwarf_hill", label: "Hill Dwarf" },
  { value: "dwarf_mountain", label: "Mountain Dwarf" },
  { value: "halfling_lightfoot", label: "Lightfoot Halfling" },
  { value: "tiefling", label: "Tiefling" },
  { value: "dragonborn", label: "Dragonborn" },
  { value: "gnome", label: "Gnome" },
  { value: "half_elf", label: "Half-Elf" },
  { value: "half_orc", label: "Half-Orc" },
];

const CLASS_OPTIONS = [
  { value: "barbarian", label: "Barbarian" },
  { value: "bard", label: "Bard" },
  { value: "cleric", label: "Cleric" },
  { value: "druid", label: "Druid" },
  { value: "fighter", label: "Fighter" },
  { value: "monk", label: "Monk" },
  { value: "paladin", label: "Paladin" },
  { value: "ranger", label: "Ranger" },
  { value: "rogue", label: "Rogue" },
  { value: "sorcerer", label: "Sorcerer" },
  { value: "warlock", label: "Warlock" },
  { value: "wizard", label: "Wizard" },
];

const BACKGROUND_OPTIONS = [
  { value: "acolyte", label: "Acolyte" },
  { value: "charlatan", label: "Charlatan" },
  { value: "criminal", label: "Criminal" },
  { value: "entertainer", label: "Entertainer" },
  { value: "folk_hero", label: "Folk Hero" },
  { value: "guild_artisan", label: "Guild Artisan" },
  { value: "hermit", label: "Hermit" },
  { value: "noble", label: "Noble" },
  { value: "outlander", label: "Outlander" },
  { value: "sage", label: "Sage" },
  { value: "sailor", label: "Sailor" },
  { value: "soldier", label: "Soldier" },
  { value: "urchin", label: "Urchin" },
];

const ALIGNMENT_OPTIONS = [
  { value: "lg", label: "Lawful Good" },
  { value: "ng", label: "Neutral Good" },
  { value: "cg", label: "Chaotic Good" },
  { value: "ln", label: "Lawful Neutral" },
  { value: "tn", label: "True Neutral" },
  { value: "cn", label: "Chaotic Neutral" },
  { value: "le", label: "Lawful Evil" },
  { value: "ne", label: "Neutral Evil" },
  { value: "ce", label: "Chaotic Evil" },
];

const ABILITY_KEYS: (keyof AbilityScores)[] = [
  "strength", "dexterity", "constitution",
  "intelligence", "wisdom", "charisma",
];

const ABILITY_LABELS: Record<keyof AbilityScores, string> = {
  strength: "STR", dexterity: "DEX", constitution: "CON",
  intelligence: "INT", wisdom: "WIS", charisma: "CHA",
};

const DEFAULT_SCORES: AbilityScores = {
  strength: 10, dexterity: 10, constitution: 10,
  intelligence: 10, wisdom: 10, charisma: 10,
};

export function CharacterCreationPage() {
  const { campaignId } = useParams<{ campaignId: string }>();
  const [step, setStep] = useState(0);
  const [saving, setSaving] = useState(false);

  // Form state — collected across all steps
  const [identity, setIdentity] = useState({ character_name: "", player_name: "" });
  const [classInfo, setClassInfo] = useState({ race: "human", char_class: "fighter", background: "outlander", alignment: "ng" });
  const [scores, setScores] = useState<AbilityScores>(DEFAULT_SCORES);
  const [backstory, setBackstory] = useState({ backstory: "", personality: "", ideals: "", bonds: "", flaws: "" });

  function handleIdentityChange(e: React.ChangeEvent<HTMLInputElement>) {
    setIdentity((p) => ({ ...p, [e.target.name]: e.target.value }));
  }

  function handleClassChange(e: React.ChangeEvent<HTMLSelectElement>) {
    setClassInfo((p) => ({ ...p, [e.target.name]: e.target.value }));
  }

  function handleScoreChange(key: keyof AbilityScores, val: string) {
    const n = Math.min(20, Math.max(1, parseInt(val) || 1));
    setScores((p) => ({ ...p, [key]: n }));
  }

  async function handleFinish() {
    setSaving(true);
    try {
      // TODO: call createPlayerCharacter(campaignId, { ...identity, ...classInfo, ability_scores: scores, level: 1, ...backstory })
      await new Promise((r) => setTimeout(r, 900));
      // navigate(`/campaigns/${campaignId}`)
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className={styles.page}>
      <div className={styles.inner}>
        <div className={styles.header}>
          <h1 className={styles.title}>Create Your Character</h1>
          <p className={styles.sub}>For Curse of Strahd · Level 3 start</p>
        </div>

        <StepProgress steps={STEPS} current={step} />

        <div className={styles.stepBody}>

          {/* Step 0 — Identity */}
          {step === 0 && (
            <div className={styles.stepSection}>
              <h2 className={styles.stepTitle}>Identity</h2>
              <div className={styles.twoCol}>
                <Input
                  label="Character name"
                  name="character_name"
                  placeholder="Arannis Moonwhisper"
                  value={identity.character_name}
                  onChange={handleIdentityChange}
                />
                <Input
                  label="Your name (player)"
                  name="player_name"
                  placeholder="Sam R."
                  value={identity.player_name}
                  onChange={handleIdentityChange}
                />
              </div>
            </div>
          )}

          {/* Step 1 — Race & Class */}
          {step === 1 && (
            <div className={styles.stepSection}>
              <h2 className={styles.stepTitle}>Race & Class</h2>
              <div className={styles.twoCol}>
                <Select label="Race" name="race" options={RACE_OPTIONS} value={classInfo.race} onChange={handleClassChange} />
                <Select label="Class" name="char_class" options={CLASS_OPTIONS} value={classInfo.char_class} onChange={handleClassChange} />
                <Select label="Background" name="background" options={BACKGROUND_OPTIONS} value={classInfo.background} onChange={handleClassChange} />
                <Select label="Alignment" name="alignment" options={ALIGNMENT_OPTIONS} value={classInfo.alignment} onChange={handleClassChange} />
              </div>
            </div>
          )}

          {/* Step 2 — Ability scores */}
          {step === 2 && (
            <div className={styles.stepSection}>
              <h2 className={styles.stepTitle}>Ability Scores</h2>
              <p className={styles.stepHint}>Enter your rolled or point-buy scores (1–20).</p>
              <div className={styles.statGrid}>
                {ABILITY_KEYS.map((key) => (
                  <div key={key} className={styles.statInputGroup}>
                    <StatBox label={ABILITY_LABELS[key]} value={scores[key]} />
                    <input
                      className={styles.statInput}
                      type="number"
                      min={1}
                      max={20}
                      value={scores[key]}
                      onChange={(e) => handleScoreChange(key, e.target.value)}
                    />
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Step 3 — Backstory */}
          {step === 3 && (
            <div className={styles.stepSection}>
              <h2 className={styles.stepTitle}>Backstory</h2>
              <Textarea
                label="Character backstory"
                placeholder="Where did they come from? What drives them?"
                value={backstory.backstory}
                onChange={(e) => setBackstory((p) => ({ ...p, backstory: e.target.value }))}
              />
              <div className={styles.twoCol}>
                <Textarea
                  label="Personality traits"
                  placeholder="How does your character behave?"
                  value={backstory.personality}
                  onChange={(e) => setBackstory((p) => ({ ...p, personality: e.target.value }))}
                />
                <Textarea
                  label="Ideals"
                  placeholder="What principles guide them?"
                  value={backstory.ideals}
                  onChange={(e) => setBackstory((p) => ({ ...p, ideals: e.target.value }))}
                />
                <Textarea
                  label="Bonds"
                  placeholder="Who or what do they care about?"
                  value={backstory.bonds}
                  onChange={(e) => setBackstory((p) => ({ ...p, bonds: e.target.value }))}
                />
                <Textarea
                  label="Flaws"
                  placeholder="What weakness holds them back?"
                  value={backstory.flaws}
                  onChange={(e) => setBackstory((p) => ({ ...p, flaws: e.target.value }))}
                />
              </div>
            </div>
          )}
        </div>

        {/* Navigation */}
        <div className={styles.navRow}>
          <Button
            variant="ghost"
            size="md"
            onClick={() => setStep((s) => s - 1)}
            disabled={step === 0}
          >
            ← Back
          </Button>
          {step < STEPS.length - 1 ? (
            <Button variant="primary" size="md" onClick={() => setStep((s) => s + 1)}>
              Continue →
            </Button>
          ) : (
            <Button variant="primary" size="md" loading={saving} onClick={handleFinish}>
              Create character
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
