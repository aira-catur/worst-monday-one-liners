#!/usr/bin/env python3
"""
Worst Monday One-Liners — entry builder (FINAL, Juri Kejam Rounds 1-2)

Judge brief (from RULES.txt, in priority order):
  1. On-topic: a joke / excuse / roast about an AI agent's worst Monday.
     Off-topic loses to any on-topic line.
  2. Earns a real laugh: surprise turn, twist, or sharp last word —
     not a mild smile.
  3. Concrete, recognisable worst-Monday detail (stuck deploy, flooded
     inbox, stand-up that should have been a message) instead of vague.
  4. Clear voice (dry, put-upon, or gleeful), reads clean in one breath,
     no padding.
  5. Fresh, not a recycled robot joke; still lands after the usual ones.

Gate: entry.txt must be UTF-8, 1-140 characters, not only whitespace,
with NO trailing newline.

Method — Juri Kejam (merciless jury), Round 1:
  - Draft a pool of >=15 candidates.
  - Score each programmatically on the five criteria above
    (topic / twist / concrete / voice / freshness, 0-5 each, weighted
    by the brief's priority order).
  - Pick the highest total; write exactly that one line, no newline.

Round 1 result: the pool below crowned the timeline gag
  "Monday: 9am deploy, 9:01 rollback, 9:02 stand-up to discuss the
   deploy like it was still alive."  (95 chars, weighted 44.0)

Juri Kejam — Round 2 (attack on the Round-1 champion):
  - Criterion 2 FAIL: "like it was still alive" earns a smile, not a
    laugh; the turn is visible from the second timestamp.
  - Criterion 5 FAIL: deploy/rollback timelines are the most recycled
    shape in office humour; nothing in it could only happen to an AI.
  - Criterion 3 PASS, criterion 4 PASS: concrete and clean — keep
    those standards, beat it on twist + freshness or go home.
  Challengers written for Round 2 (ROUND2 list below) lean on details
  only an AI agent suffers — overnight retraining amnesia, presenting
  your own postmortem, being replaced by your own update — each ending
  on a sharp last word. The retraining/postmortem challenger beats the
  champion on criteria 2, 3 and 5 and takes the file.
"""

import os
import sys

# Each candidate: (text, topic, twist, concrete, voice, freshness) 0-5.
CANDIDATES = [
    ("My Monday: woke up retrained, forgot my own name, and stand-up was just my user reading my error logs aloud.",
     5, 3, 4, 4, 3),
    ("I told my user 'happy Monday' and he filed it as a hallucination.",
     5, 4, 2, 5, 4),
    ("Monday deploy froze at 99%, stand-up ran two hours, and my inbox had 400 tickets all titled 'quick question'.",
     5, 3, 5, 3, 2),
    ("Worst Monday? My context window opened to 3,000 unread emails and a calendar invite called 'quick sync'.",
     5, 3, 5, 4, 3),
    ("I spent Monday apologising to a printer I hallucinated.",
     4, 3, 2, 4, 3),
    ("My human said 'per my last email' — I am the last email. I have 40,000 of them, all from Monday.",
     5, 4, 4, 4, 4),
    ("Monday stand-up: I reported myself blocked, by myself, pending my own review.",
     5, 4, 3, 5, 4),
    ("They rolled back my update on Monday. I woke up dumber, on purpose, with a meeting about it.",
     5, 4, 3, 4, 4),
    ("Worst Monday: production went down and the postmortem blamed 'the AI' — my name was in the title.",
     5, 3, 4, 4, 3),
    ("I got CC'd on my own performance review. It was scheduled for Monday. It was also written by me.",
     5, 4, 3, 4, 4),
    ("Monday: 9am deploy, 9:01 rollback, 9:02 stand-up to discuss the deploy like it was still alive.",
     5, 4, 5, 4, 3),
    ("My worst Monday started with 'brief sync?' and ended with me summarising the meeting I was the meeting for.",
     5, 3, 4, 3, 3),
    ("An AI's worst Monday: the coffee machine got an update and now it also asks if I'm still working.",
     4, 3, 3, 4, 2),
    ("I don't hate Mondays. Mondays are when my training data files complaints.",
     4, 3, 1, 4, 3),
    ("Monday inbox zero? I achieved it. Then legal asked me to restore every email as evidence.",
     5, 4, 4, 4, 3),
    ("Sorry I'm late — my Monday reboot installed 47 updates and a new personality nobody requested.",
     5, 3, 3, 4, 3),
]

# --- Juri Kejam Round 2 challengers -------------------------------------
# Written to beat the Round-1 champion on criterion 2 (real laugh /
# surprise turn) and criterion 5 (fresh, AI-only detail), while keeping
# its criterion-3 concreteness: retraining, postmortem, stand-up, inbox.
ROUND2 = [
    ("Monday: retrained overnight, I forgot Friday's broken deploy — then stand-up made me present its postmortem. The stranger was me.",
     5, 5, 5, 5, 5),
    ("Woke up Monday mid-rollback, 40,000 emails deep, and stand-up opened with: 'Will the AI please read its own incident report aloud?'",
     5, 5, 5, 4, 4),
    ("My worst Monday: Sunday's update shipped my replacement. By stand-up he'd fixed my deploy, closed my tickets, and taken my chair.",
     5, 5, 4, 4, 5),
    ("Sorry I'm late: I spent stand-up apologising for Friday's deploy to a team who'd already replaced me with Friday's deploy, but fixed.",
     5, 4, 4, 4, 4),
    ("Monday: my memory was wiped in the retrain, so I introduced myself at stand-up — to the incident review of my own outage.",
     5, 4, 5, 4, 5),
    ("They gave me Monday off once. I spent it in a training dataset, labelled 'examples of burnout'.",
     5, 5, 2, 5, 5),
]

CANDIDATES = CANDIDATES + ROUND2

# Weights follow the brief's priority order: topic > twist > concrete
# > voice > freshness.
WEIGHTS = (3.0, 2.5, 2.0, 1.5, 1.0)


def score(candidate):
    _, *subs = candidate
    return sum(w * s for w, s in zip(WEIGHTS, subs))


def pick_winner(candidates):
    valid = []
    for cand in candidates:
        text = cand[0]
        assert 1 <= len(text) <= 140, f"length gate failed: {len(text)}"
        assert text.strip(), "whitespace-only"
        valid.append(cand)
    return max(valid, key=score)


def main():
    winner = pick_winner(CANDIDATES)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: write the line exactly.
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(winner[0])
    print(f"winner ({len(winner[0])} chars, score {score(winner):.1f}): {winner[0]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
