---
name: AI Study Buddy
colors:
  surface: '#faf8ff'
  surface-dim: '#d9d9e5'
  surface-bright: '#faf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f3fe'
  surface-container: '#ededf9'
  surface-container-high: '#e7e7f3'
  surface-container-highest: '#e1e2ed'
  on-surface: '#191b23'
  on-surface-variant: '#434655'
  inverse-surface: '#2e3039'
  inverse-on-surface: '#f0f0fb'
  outline: '#737686'
  outline-variant: '#c3c6d7'
  surface-tint: '#0053db'
  primary: '#004ac6'
  on-primary: '#ffffff'
  primary-container: '#2563eb'
  on-primary-container: '#eeefff'
  inverse-primary: '#b4c5ff'
  secondary: '#5c5f61'
  on-secondary: '#ffffff'
  secondary-container: '#e0e3e5'
  on-secondary-container: '#626567'
  tertiary: '#943700'
  on-tertiary: '#ffffff'
  tertiary-container: '#bc4800'
  on-tertiary-container: '#ffede6'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dbe1ff'
  primary-fixed-dim: '#b4c5ff'
  on-primary-fixed: '#00174b'
  on-primary-fixed-variant: '#003ea8'
  secondary-fixed: '#e0e3e5'
  secondary-fixed-dim: '#c4c7c9'
  on-secondary-fixed: '#191c1e'
  on-secondary-fixed-variant: '#444749'
  tertiary-fixed: '#ffdbcd'
  tertiary-fixed-dim: '#ffb596'
  on-tertiary-fixed: '#360f00'
  on-tertiary-fixed-variant: '#7d2d00'
  background: '#faf8ff'
  on-background: '#191b23'
  surface-variant: '#e1e2ed'
  oxford-blue: '#1E293B'
  success-green: '#059669'
  warning-red: '#DC2626'
  border-subtle: '#E2E8F0'
typography:
  headline-xl:
    fontFamily: Hanken Grotesk
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-xl-mobile:
    fontFamily: Hanken Grotesk
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 34px
  headline-lg:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-caps:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
  button:
    fontFamily: Hanken Grotesk
    fontSize: 15px
    fontWeight: '600'
    lineHeight: 20px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  container-max: 1200px
  gutter: 1.5rem
  margin-mobile: 1rem
  stack-sm: 0.5rem
  stack-md: 1.5rem
  stack-lg: 3rem
---

## Brand & Style

The design system is built for **AI Study Buddy**, focusing on an "Academic Minimalist" aesthetic. The goal is to provide a "no-mess" environment that reduces cognitive load for students, mirroring the focused utility of Notion and the structured clarity of Khan Academy.

The style is **Minimalist with Subtle Tonal Depth**. It leverages heavy white space, a strictly organized information hierarchy, and professional, high-contrast typography. It avoids unnecessary decoration, using subtle shadows and crisp borders only to define functional zones. The personality is intellectual, dependable, and quietly intelligent, evoking a sense of calm focus and scholarly achievement.

## Colors

The palette is anchored in a sophisticated **Scholar Blue** (#2563EB) and a spectrum of architectural grays. 

- **Primary:** Used for key actions, active states, and focus indicators. 
- **Secondary:** A soft background tint used for card surfaces and subtle grouping.
- **Neutral/Oxford Blue:** Used for high-contrast typography and iconography to ensure legibility.
- **Semantic Colors:** Success (Green) is used for correct quiz answers; Warning (Red) is used for weak topics and errors.

The interface primarily utilizes a **light mode** default to simulate the clarity of paper and traditional study environments.

## Typography

This design system uses a multi-font approach to create a rigorous hierarchy:
- **Headlines:** Uses **Hanken Grotesk**. Its sharp, contemporary feel provides a professional "EdTech" look.
- **Body:** Uses **Inter** for maximum readability in long-form notes and AI responses.
- **Data/Labels:** Uses **JetBrains Mono** for metadata, session IDs, and technical labels, reinforcing the "AI" and "Agent" nature of the tool.

Text should be primarily Oxford Blue (#1E293B) for maximum contrast against the white/gray backgrounds.

## Layout & Spacing

The layout follows a **Fixed Grid** model for desktop, centered to create a focused reading experience similar to a document editor. 

- **Desktop (1200px+):** 12-column grid with a 300px fixed sidebar for navigation and session management.
- **Tablet (768px - 1024px):** 8-column grid; sidebar collapses into a drawer.
- **Mobile (< 768px):** Single column fluid layout with 16px horizontal margins.

Spacing follows a strict vertical rhythm based on 8px increments. Use `stack-lg` to separate major sections (like Chat vs. Input) and `stack-sm` for related items (like Question vs. Multiple Choice options).

## Elevation & Depth

To maintain the "minimal" aesthetic, elevation is achieved through **Tonal Layering** and **Low-Contrast Outlines** rather than heavy shadows.

- **Level 0 (Background):** White (#FFFFFF).
- **Level 1 (Cards/Sidebar):** Secondary Blue-Gray (#F8FAFC) with a subtle 1px border (#E2E8F0).
- **Level 2 (Active/Floating):** White background with a very soft, high-diffusion shadow (0px 4px 12px rgba(0, 0, 0, 0.05)).

Interactive elements like Quiz cards should feel "raised" on hover using a subtle shift in border color rather than a large shadow.

## Shapes

The design system uses a **Soft (0.25rem)** roundedness profile. This creates a professional, "crisp" appearance that feels modern but retains the structural integrity of an academic tool.

- **Standard Elements:** 4px (0.25rem) radius for buttons, input fields, and small cards.
- **Large Containers:** 8px (0.5rem) radius for main content areas or file upload zones.
- **Status Pills:** Fully rounded (pill-shaped) for "Weak Topic" tags or "Easy/Hard" difficulty badges.

## Components

### Buttons
- **Primary:** Solid Oxford Blue or Scholar Blue with white text. 4px roundedness.
- **Secondary:** Ghost style (border only) or subtle gray background for "Export CSV" or "Flip Card" actions.

### Cards (Flashcards & Quiz)
- Flashcards use a minimal Level 1 surface. On "flip," use a subtle CSS transition rather than a hard jump.
- Quiz questions are grouped in Level 1 containers with `stack-md` spacing between them.

### Input Fields
- Understated 1px borders (#E2E8F0). Focus state uses a 2px Scholar Blue outline.
- Chat input should be pinned to the bottom of the viewport with a subtle backdrop blur to separate it from the scrolling history.

### Progress & Charts
- Use the Success Green for positive scores and Warning Red for "Weak Topics."
- Progress bars should be slim (8px height) to maintain the minimalist feel.

### Sidebar
- Use a high-contrast treatment (dark background or very distinct gray) to differentiate navigation and session management from the primary "study" workspace.