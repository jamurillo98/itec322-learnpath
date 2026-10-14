# Colour Theme Shortlist — LearnPath

This document records the colour themes considered for the LearnPath UI and
the final team decision.

---

## Final approved theme — Calm Teal & Navy
Calm Teal & Navy is the team's approved theme: trustworthy, modern, and
friendly. It supports clarity and approachability in an educational product.

- Primary (brand): #0EA5A4
- Dark / header: #05445E
- Accent / highlights: #06B6D4
- Background: #F8FAFC
- Surface (cards): #FFFFFF
- Text primary: #0F172A
- Text muted: #64748B

Why: good contrast, a professional but warm feel, and easy to use for CTAs and info states.

CSS variables (copy-paste):
:root {
  --lp-primary: #0EA5A4;
  --lp-primary-dark: #05445E;
  --lp-accent: #06B6D4;
  --lp-bg: #F8FAFC;
  --lp-surface: #FFFFFF;
  --lp-text: #0F172A;
  --lp-muted: #64748B;
}

---

## Option A — Vibrant Orange & Purple (Energetic)
Use-case: upbeat, youthful, good for marketing-focused CTAs and energetic flows.

- Primary: #FB923C
- Secondary (accent): #8B5CF6
- Dark: #5B21B6
- Background: #FFFBEB
- Surface: #FFFFFF
- Text primary: #0F172A
- Text muted: #6B7280

Notes: high-energy; ensure CTA text contrast on solid fills.

---

## Option B — Minimal Blue-Gray (Clean / Neutral)
Use-case: professional, neutral, easy to extend for many content types.

- Primary: #2563EB
- Dark: #1E3A8A
- Accent: #64748B
- Background: #F1F5F9
- Surface: #FFFFFF
- Text primary: #0F172A
- Text muted: #6B7280

Notes: conservative and highly legible; good for academic audiences.

---

## Option C — Warm Purple & Coral (Friendly & Modern)
Use-case: modern, slightly playful, good when you want warmth without being too loud.

- Primary: #7C3AED
- Accent: #FB7185
- Dark: #4C1D95
- Background: #FEF2F8
- Surface: #FFFFFF
- Text primary: #0F172A
- Text muted: #6B7280

Notes: cohesive and contemporary — test small text contrast for accessibility.

---

## Accessibility notes (applies to all palettes)
- Aim for contrast ratios >= 4.5:1 for normal body text and >= 3:1 for large text.
- Use the darkest text color on the light surfaces; use white (#FFFFFF) for CTA text only when contrast is sufficient.
- Test interactive states (hover, focus, disabled) and ensure focus outlines remain visible.

---

## Decision and implementation
The team approved Calm Teal & Navy in Sprint 2. The frontend applies the
palette in `frontend/src/theme.css`; navy is used for buttons and the header,
while teal and cyan provide accents. The implementation uses the accessibility
guidance above, including sufficient contrast for button text.