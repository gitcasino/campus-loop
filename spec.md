# CampusLoop

## Product & Engineering Specification

**Course:** 22AIE205 — Introduction to Python  
**Project:** CampusLoop  
**Application type:** Browser-based campus resource-sharing application  
**Primary stack:** Python + Streamlit + Pandas + NumPy + Plotly  
**Persistence:** CSV  
**Package management:** uv  
**Design direction:** Dark, premium, cinematic, glass, motion-heavy, 3D-enhanced

---

# 1. What We Are Building

CampusLoop is a campus resource-sharing product.

A student who needs something should be able to find something already available on campus instead of buying another one. A student who owns something they barely use should be able to put it into circulation.

The product supports four sharing modes:

- Borrow
- Lend
- Swap
- Give Away

The application combines the actual sharing workflow with the academic requirements of the Python project:

- CSV-backed data
- CRUD
- Pandas
- NumPy
- dynamic visualization
- search/filter/sort
- explainable matching
- reporting
- object-oriented Python
- exception handling

The application must feel like a real student product first and a classroom project second.

---

# 2. The Product Experience

The central loop is:

```text
Need something
      ↓
Discover
      ↓
Inspect
      ↓
Choose a sharing option
      ↓
Start / record the activity
      ↓
Complete the activity
      ↓
See the resulting activity and impact
```

For someone offering an item:

```text
Have something useful
      ↓
Create listing
      ↓
Publish it
      ↓
Someone discovers it
      ↓
Sharing activity is recorded
      ↓
Item continues circulating
```

The interface should make these flows obvious without requiring the user to understand the implementation.

---

# 3. Product Personality

CampusLoop should feel:

- calm;
- premium;
- modern;
- environmental without looking like an environmental NGO website;
- tactile;
- spatial;
- confident;
- fast;
- slightly futuristic;
- campus-native.

It should **not** feel like:

- a default Streamlit dashboard;
- an admin panel;
- a Bootstrap template;
- a generic AI landing page;
- a neon cyberpunk website;
- a 3D demo with a spreadsheet attached;
- a collection of disconnected academic pages.

The visual system should communicate that physical objects are moving through a campus community.

---

# 4. Visual Reference

Use:

```text
assets/campus-loop.png
```

as the primary visual reference.

Before implementing the interface, inspect the asset and extract its visual language:

- lighting;
- palette;
- object treatment;
- depth;
- atmosphere;
- composition;
- illustration style;
- typography mood.

Do not copy the image literally.

Use it as the visual source of truth for the product's character.

---

# 5. Design System

## 5.1 Overall mode

CampusLoop is dark-only.

There is no light-mode switch in the final product.

## 5.2 Base palette

Starting palette:

```text
Background:       #050A0A
Surface:          #0B1415
Primary green:    #8CFF66
Secondary green:  #38D996
Soft green:       #B8FF9A
Primary text:     #F4F7F5
Muted text:       #9AA7A0
Warm accent:      #D6A84F
```

These are starting tokens, not excuses to fill every surface with green.

Green should identify action, availability, progress and positive state.

## 5.3 Surfaces

Use a small number of surface levels:

```text
background
surface
raised surface
glass surface
overlay
```

Glass should be subtle:

- translucent;
- thin border;
- controlled blur;
- slight inner highlight;
- enough contrast for text.

Avoid making every element a floating glass card.

## 5.4 Shape language

Use:

- large but controlled corner radii;
- thin borders;
- consistent spacing;
- clear alignment;
- restrained shadows.

Avoid:

- excessive pill-shaped containers;
- nested cards inside cards inside cards;
- random corner radii.

---

# 6. Typography

The hierarchy should be immediately readable.

```text
Eyebrow / context
Page title
Supporting sentence
Primary action
Section title
Record title
Metadata
Supporting detail
```

Headings should have presence.

Body copy should remain quiet.

Numbers should be easy to scan.

Do not turn every label into uppercase micro-text.

---

# 7. Navigation

Primary navigation:

```text
Home
Discover
My Listings
Sharing
Users
Impact
Analytics
```

The navigation is product navigation, not dataset navigation.

The active page must be unmistakable.

Secondary controls belong inside the relevant page.

Do not create a sidebar containing every possible operation.

---

# 8. Home

Home answers three questions immediately:

1. What is CampusLoop?
2. What can I do here?
3. What is happening on campus right now?

## Above the fold

The first viewport should contain:

- brand;
- short product statement;
- primary discovery action;
- a strong visual/3D product moment;
- a small amount of live platform information.

Suggested headline direction:

```text
What you need
might already be here.
```

The exact copy can be refined during implementation.

## Live information

Use real CSV-derived values for a small set of useful facts, such as:

- available listings;
- active sharing activity;
- number of categories;
- recent reuse activity.

Do not create a wall of KPI cards.

## Recent activity

Show a restrained feed derived from real sharing records.

The feed should look like product activity, not raw CSV rows.

---

# 9. Discover

Discover is the primary everyday screen.

The page should prioritize:

```text
Search
Filters
Results
```

not analytics.

## Search

Search the real listing fields that contain useful text.

Search must:

- be case-insensitive;
- support partial matches;
- work with an empty query;
- return a useful zero-result state.

## Filters

Expose filters supported by the actual schema:

- category;
- sharing mode;
- availability;
- location.

Add other filters only when the data supports them.

## Sorting

Provide useful human-facing choices, for example:

- newest;
- recently updated;
- availability;
- relevance.

Do not expose every raw database column as a sort option.

## Results

A result should communicate:

```text
Item
Category
Condition
Sharing mode
Availability
Location
Owner
Primary action
```

The full record belongs in the detail experience.

---

# 10. Listing Detail

The detail view is where a user decides whether an item is useful.

The hierarchy should be:

```text
Item name
Status
Short description

Key facts
Sharing terms
Location
Owner
Relevant dates

Primary action
Secondary actions
```

The primary action depends on the record.

Examples:

```text
Borrow     → Request / start activity
Lend       → Start sharing
Swap       → Find compatible item
Give Away  → Request / receive
```

Never show an action that the underlying data cannot support.

---

# 11. My Listings

Dataset:

```text
data/item_listings.csv
```

Owner:

```text
Rahul
```

This is one of Rahul's main academic vertical slices.

The page must support:

- create;
- read;
- update;
- delete;
- search/filter/sort;
- analytics;
- dynamic charts.

The user experience should be:

```text
My inventory
     ↓
Choose record
     ↓
View / edit / delete
```

Creation should be a focused form, not a 30-field wall.

Required fields from the academic specification must be represented using controls appropriate to their type.

---

# 12. Sharing

Dataset:

```text
data/sharing_activities.csv
```

Owner:

```text
Rahul
```

This page represents actual sharing activity.

Important distinction:

```text
Item listing = something available
Sharing activity = something that happened / is being tracked
```

The page should support:

- activity list;
- activity detail;
- create;
- read;
- update;
- delete;
- filtering;
- sorting;
- analytics;
- charts.

Where the dataset contains linked IDs, the UI should resolve them into understandable item/user information.

---

# 13. Users

Dataset:

```text
data/users.csv
```

Owner:

```text
Charan
```

The page should provide:

- searchable user records;
- readable user detail;
- CRUD;
- relevant participation information;
- required statistics;
- required dynamic visualizations.

Simulated student identities are acceptable.

Do not introduce production authentication.

---

# 14. Impact

Dataset:

```text
data/impact.csv
```

Owner:

```text
Abhiram
```

Impact should answer:

> What effect did the sharing activity have according to our data?

Use real stored values and transparent calculations.

Possible indicators include:

- items shared;
- reuse activity;
- estimated purchases avoided;
- category contribution;
- other indicators represented by the actual dataset.

If a metric is estimated, label it as estimated.

Do not present assumptions as scientific measurements.

---

# 15. Analytics

Analytics is an interpretation layer over the actual data.

Every analytical surface should answer:

```text
What is being measured?
From which records?
Under which filters?
Why does it matter?
```

Required per academic dataset/page:

- at least 3 meaningful statistics;
- at least 2 dynamic chart types;
- search/filter/sort;
- explicit missing-data treatment.

## Chart selection

Use the chart that answers the question.

Examples:

```text
Category comparison → bar chart
Time trend          → line chart
Distribution        → histogram
Simple composition  → donut/pie only when appropriate
```

Do not use a donut chart merely because it looks attractive.

## Filter consistency

If the user filters records:

```text
records
metrics
charts
report context
```

must all describe the same filtered population.

---

# 16. Smart Matching

Matching is a deterministic product feature.

It should help a user find the most suitable listing based on information actually available in the data.

Possible factors:

- category/item compatibility;
- availability;
- location;
- sharing mode;
- condition;
- relevant date/duration;
- other supported listing attributes.

The implementation must produce a score and reasons.

Example presentation:

```text
92% match

Scientific Calculator

Available now
Good condition
Engineering block

Why it matches
✓ Same category
✓ Available
✓ Compatible sharing mode
✓ Same location
```

The exact scoring formula should be simple enough for a student to explain during evaluation.

Do not use an external AI service for the core matching algorithm.

Do not call it “AI-generated”.

---

# 17. CRUD

CRUD must operate on the CSV source of truth.

## Create

Flow:

```text
Open form
→ enter values
→ validate
→ create record
→ save CSV
→ reload/verify
→ show success
```

## Read

Read includes:

- list;
- search;
- filter;
- sort;
- detail.

## Update

Flow:

```text
Choose record
→ edit
→ validate
→ save
→ reload
→ show updated state
```

## Delete

Flow:

```text
Choose record
→ delete
→ confirm
→ save
→ reload
→ show deleted state
```

Cancellation must not alter the record.

---

# 18. Persistence

CSV is the persistent source of truth.

A write operation should be treated as a transaction:

```text
Read current data
→ validate requested change
→ apply change in memory
→ validate resulting data
→ write safely
→ reload
→ verify
```

If writing fails:

- preserve the last valid CSV;
- do not report success;
- show a useful user-facing error.

Session state may hold temporary UI state, but it must never become the database.

---

# 19. Data Integrity

Before coding the UI, inspect the actual four CSVs.

Determine:

- exact columns;
- ID columns;
- relationships;
- data types;
- categorical values;
- dates;
- numeric fields;
- missing-value patterns.

Do not invent columns because a UI mockup would look better with them.

Validate:

- required fields;
- IDs;
- duplicate IDs;
- data types;
- dates;
- numeric ranges;
- categorical values;
- related IDs where relationships exist.

Missing data must have an explicit policy.

---

# 20. Current Data Domains

The repository uses:

```text
data/
├── users.csv
├── item_listings.csv
├── sharing_activities.csv
└── impact.csv
```

Current project scale:

```text
users.csv               ~1,000 records
item_listings.csv       ~5,000 records
sharing_activities.csv  ~8,000 records
impact.csv              ~8,000 records
```

These are real project datasets.

Do not replace them with generated demo data.

---

# 21. Academic Ownership

The application is one product, but dataset ownership remains visible for evaluation.

```text
Rahul
├── item_listings.csv
└── sharing_activities.csv

Charan
└── users.csv

Abhiram
└── impact.csv
```

Each owner must be able to demonstrate:

- their schema;
- their class;
- CRUD;
- validation;
- persistence;
- Pandas analysis;
- NumPy usage where appropriate;
- charts;
- error handling.

Shared UI components are encouraged.

Shared ownership of the academic implementation is not a substitute for individual understanding.

---

# 22. Python Architecture

Keep the application understandable.

Suggested structure:

```text
campus-loop/
├── app.py
├── pages/
│   ├── home.py
│   ├── discover.py
│   ├── listings.py
│   ├── sharing.py
│   ├── users.py
│   ├── impact.py
│   └── analytics.py
├── core/
│   ├── models.py
│   ├── repositories.py
│   ├── validation.py
│   ├── analytics.py
│   ├── matching.py
│   └── reporting.py
├── ui/
│   ├── components.py
│   ├── cards.py
│   ├── charts.py
│   ├── navigation.py
│   └── styles.css
├── components/
│   └── motion/
├── assets/
│   ├── campus-loop.png
│   └── 3d/
├── data/
│   ├── users.csv
│   ├── item_listings.csv
│   ├── sharing_activities.csv
│   └── impact.csv
├── tests/
├── reports/
├── .streamlit/
│   └── config.toml
├── pyproject.toml
├── uv.lock
├── requirements.txt
├── README.md
└── spec.md
```

This is a starting point, not an excuse to create empty modules.

Keep code where it is easiest to understand.

---

# 23. Object-Oriented Design

Use classes for real responsibilities.

Reasonable examples:

```text
CsvRepository
ListingRepository / ListingManager
SharingActivityRepository / SharingActivityManager
UserRepository / UserManager
ImpactRepository / ImpactManager
MatchingEngine
ReportBuilder
```

Do not create classes that contain one trivial method just to satisfy an OOP checkbox.

The class design should be explainable during a viva.

---

# 24. Data Layer

The data layer should centralize:

- loading;
- validation;
- record creation;
- record updates;
- record deletion;
- safe persistence.

Pages should not each implement their own CSV-writing logic.

Avoid duplicated code such as:

```python
pd.read_csv(...)
```

and

```python
to_csv(...)
```

scattered throughout every page.

---

# 25. Analytics Layer

Analytics functions should be separate from presentation.

Preferred flow:

```text
CSV
 ↓
Repository
 ↓
DataFrame
 ↓
Validation / cleaning
 ↓
Filter
 ↓
Analysis
 ↓
Chart
```

This makes the Pandas/NumPy work easy to demonstrate.

Charts should not contain business logic.

---

# 26. Reporting

Provide a useful summary report for relevant dataset views.

A report should include:

- timestamp;
- dataset/view;
- row count;
- active filters;
- relevant summary statistics;
- relevant current information.

The simplest reliable format is acceptable.

Do not spend project time building an elaborate reporting engine before CRUD and analytics work.

---

# 27. Error Handling

Expected failures must not crash the application.

Handle:

- missing CSV;
- empty CSV;
- malformed CSV;
- invalid values;
- duplicate IDs;
- invalid IDs;
- invalid update;
- invalid delete;
- missing values;
- failed writes.

Normal users should see messages such as:

```text
Couldn't save this listing.

Your existing data is still intact.
Check the highlighted fields and try again.
```

not Python tracebacks.

During development, errors may be logged for debugging.

---

# 28. Motion Is Part of the Product

CampusLoop is intentionally animation-heavy.

Animation is not an optional final polish pass.

The application should have a coherent motion language across:

- navigation;
- page entrance;
- discovery;
- cards;
- filters;
- forms;
- CRUD feedback;
- matching;
- charts;
- impact;
- 3D.

The goal is to make the interface feel alive and spatial, not to make everything constantly move.

---

# 29. Motion Hierarchy

Use four levels.

## Ambient

Slow, almost unnoticed:

- environmental light;
- 3D movement;
- subtle depth;
- background parallax.

## Structural

Medium-speed:

- page entrance;
- section reveal;
- navigation transitions;
- result layout changes.

## Interactive

Fast:

- hover;
- focus;
- press;
- filter changes;
- control feedback.

## Transactional

Clear:

- saved;
- deleted;
- failed;
- matched;
- status changed.

A save confirmation should feel immediate.

A background environment should never steal attention.

---

# 30. Animation Style

Motion should feel:

- smooth;
- physical;
- restrained;
- intentional;
- premium.

Use:

- transform;
- opacity;
- scale;
- clip/mask transitions where useful;
- stagger;
- controlled easing;
- timeline sequencing;
- subtle depth.

Avoid:

- bouncing everything;
- excessive spring effects;
- random delays;
- infinite floating cards;
- giant page transitions;
- animations that delay interaction;
- animations that cause layout shifts.

---

# 31. GSAP / Web Motion

The project already contains motion-focused skills.

Use them deliberately.

Good candidates:

```text
GSAP core
GSAP timelines
ScrollTrigger
GSAP performance utilities
Web motion patterns
```

Do not use every plugin simply because it exists.

A motion library is justified when CSS alone cannot provide the required choreography.

---

# 32. 3D Experience

3D is a major part of the visual identity.

The strongest use should be the Home experience.

The mental model:

```text
A shared campus environment
with useful objects moving through it.
```

Good 3D elements may include:

- campus structures;
- books;
- calculators;
- bags;
- chargers;
- sports equipment;
- boxes;
- subtle particles;
- light;
- depth layers.

The exact assets should be selected to fit the poster reference and actual product identity.

3D should create depth and identity.

It should not become the task itself.

---

# 33. 3D Placement

Prioritize 3D here:

```text
Home hero
Major transition moments
Selected empty states / ambient surfaces
```

Do not force 3D into:

```text
Dense tables
CRUD forms
Every card
Every chart
Every button
```

The more information-dense the screen, the quieter the 3D should become.

---

# 34. 3D Performance

The application must remain usable on a normal student laptop.

Therefore:

- lazy-load heavy scenes when practical;
- use reasonable geometry;
- avoid unnecessary physics;
- limit particle counts;
- avoid continuous CPU-heavy calculations;
- pause or simplify background animation when not visible;
- use GPU-friendly transforms;
- provide a non-3D fallback.

A failed 3D layer must never prevent the Python application from working.

---

# 35. Streamlit + Frontend Boundary

Streamlit remains the application framework.

Custom HTML/CSS/JavaScript and Streamlit custom components may be used for experiences that native Streamlit cannot provide, including sophisticated motion and 3D. Streamlit's current custom-component system supports HTML, CSS, JavaScript and bidirectional communication, making it appropriate for this presentation layer. citeturn0search0turn0search5

Use the browser layer for:

- motion;
- 3D;
- premium visual components;
- specialized interactions.

Use Python for:

- data;
- CRUD;
- validation;
- matching;
- analytics;
- reporting.

The browser layer must not become a second application with duplicated business logic.

---

# 36. Frontend Safety

Any custom HTML/JavaScript must be treated as trusted application code.

Do not inject unsanitized user-controlled data directly into executable HTML or JavaScript. Streamlit explicitly warns that custom component JavaScript runs with page-level privileges. citeturn0search1

Escape dynamic text before rendering it into custom HTML.

---

# 37. Accessibility

Support:

```text
prefers-reduced-motion
```

When enabled:

- remove ambient animation;
- reduce parallax;
- shorten transitions;
- preserve interaction feedback;
- preserve readable state.

Also provide:

- keyboard focus;
- meaningful labels;
- readable contrast;
- non-color-only status;
- understandable chart labels.

Animation must never be the only way a user knows that something happened.

---

# 38. Responsive Layout

Primary target:

```text
Laptop / desktop browser
Classroom projector
```

Still support narrower screens sensibly.

At smaller widths:

- cards reflow;
- navigation remains usable;
- controls stack;
- tables can scroll horizontally;
- 3D reduces complexity;
- decorative layers may disappear.

Do not create a separate mobile codebase.

---

# 39. Realistic Interface Patterns

Use familiar product patterns.

Examples:

### Search

Large enough to be useful, not a tiny input buried in a dashboard.

### Filter

Persistent enough to understand what is active.

### Forms

Grouped by meaning rather than by database column order.

### Tables

Used when comparison matters.

### Cards

Used when scanning individual items matters.

### Detail pages

Used when making a decision matters.

### Modals / confirmations

Used for destructive or consequential actions.

The UI should feel designed around tasks rather than database tables.

---

# 40. Empty States

Every important data surface needs an intentional empty state.

Examples:

```text
No items match your filters.

Try removing a filter or searching for another item.
```

or:

```text
No sharing activity yet.

Once a sharing record is created, it will appear here.
```

Never show an unexplained empty chart or empty table.

---

# 41. Loading States

Loading should be quiet.

Use:

- skeletons;
- subtle fades;
- placeholders;
- progress feedback only when a real operation takes long enough to justify it.

Do not show fake loading progress.

---

# 42. Success States

Success should answer:

```text
What happened?
```

Examples:

```text
Listing created
Listing updated
Activity recorded
Changes saved
Record deleted
```

Keep the feedback visible long enough to be understood but do not obstruct the next task.

---

# 43. Visual Data Presentation

Plotly should be the default interactive visualization choice where suitable.

Charts should:

- match the dark product environment;
- use restrained colors;
- have readable labels;
- have useful hover information;
- resize correctly;
- respond to filters.

The chart should look like part of CampusLoop, not a pasted Plotly example.

---

# 44. Performance Rules

Optimize in this order:

```text
Correctness
→ Reliability
→ Usability
→ Responsiveness
→ Visual quality
→ Motion richness
→ Decorative complexity
```

Do not sacrifice data correctness for visual effects.

Avoid:

- unnecessary repeated CSV reads;
- enormous DOM trees;
- unbounded animation loops;
- oversized 3D assets;
- unnecessary network dependencies.

Caching may be used for read-heavy data, but writes must invalidate or refresh stale cached data.

---

# 45. UV Setup

The project uses uv.

Expected files:

```text
pyproject.toml
uv.lock
requirements.txt
```

Run the application with:

```bash
uv run streamlit run app.py
```

Keep `requirements.txt` aligned with the dependencies actually required by the project.

Use relative paths.

Do not hardcode a developer's home directory.

---

# 46. Skills Available to the Build Agent

The project already contains:

```text
.agents/skills/
├── frontend-design
├── 3d-website-architect
├── developing-with-streamlit
├── web-design-guidelines
├── data-visualization
├── data-analysis
├── web-motion
├── gsap-core
├── gsap-timeline
├── gsap-scrolltrigger
├── gsap-plugins
├── gsap-utils
├── gsap-performance
└── gsap-react
```

Use the relevant skills before making architecture or visual decisions.

Do not add another skill unless a real missing capability is discovered.

---

# 47. Implementation Order

Build in this order.

## Step 1 — Understand the project

Inspect:

```text
spec.md
data/users.csv
data/item_listings.csv
data/sharing_activities.csv
data/impact.csv
assets/campus-loop.png
```

Also inspect the existing repository and installed skills.

Do not start by guessing the schema.

## Step 2 — Establish the data layer

Implement:

- CSV loading;
- validation;
- repository classes;
- safe persistence;
- shared error handling.

## Step 3 — Make CRUD real

Complete the four academic vertical slices:

```text
Listings
Sharing
Users
Impact
```

Test persistence after every write.

## Step 4 — Build discovery

Implement:

- search;
- filters;
- sorting;
- detail view.

## Step 5 — Add matching

Implement the deterministic scoring model and visible reasons.

## Step 6 — Add analytics

Implement the required statistics and charts from the real data.

## Step 7 — Build the product UI

Only after the underlying workflows work:

- establish design system;
- navigation;
- cards;
- forms;
- tables;
- empty states;
- error states.

## Step 8 — Add motion

Add motion to the already-working interfaces.

## Step 9 — Add 3D

Build the strongest 3D experience around Home and selected product moments.

## Step 10 — Final QA

Run the whole product from a clean start.

---

# 48. Testing

## CRUD

For each dataset test:

```text
Create valid
Create invalid
Create duplicate ID
Read
Update valid
Update invalid
Delete valid
Delete invalid
Cancel delete
Refresh application
Confirm persistence
```

## Data failures

Test:

```text
Missing CSV
Empty CSV
Malformed CSV
Missing values
Wrong data type
Invalid ID
Broken relationship
Failed write
```

## Analytics

Test:

```text
Normal data
Filtered data
Zero-result filter
Missing values
Small dataset
Date range
```

Charts must remain valid when the filtered population changes.

## Matching

Test:

```text
Strong match
Partial match
No match
Unavailable listing
Tied scores
Missing optional attributes
```

Reasons shown to the user must correspond to the actual scoring logic.

---

# 49. Motion QA

Test motion in the running application.

Check:

- first load;
- navigation;
- hover;
- focus;
- search;
- filter;
- form submission;
- save;
- delete;
- chart transitions;
- matching;
- resize;
- reduced motion.

Look specifically for:

- flicker;
- jumps;
- clipping;
- layout shift;
- stale animation;
- scroll problems;
- animation blocking clicks;
- console/runtime errors.

---

# 50. 3D QA

Check:

- first load;
- camera composition;
- frame rate;
- resize;
- scrolling;
- interaction with content;
- reduced motion;
- fallback behavior.

The 3D scene must remain subordinate to the product task.

---

# 51. Demo Story

The final demo should be a single story, not a tour of random pages.

```text
Open CampusLoop
      ↓
See what is happening
      ↓
Discover an item
      ↓
Search / filter
      ↓
Open item
      ↓
Show matching
      ↓
Create or update a listing
      ↓
Show that the CSV changed
      ↓
Open sharing activity
      ↓
Show analytics
      ↓
Show impact
      ↓
Show report
      ↓
Explain dataset ownership
```

The evaluator should see both:

```text
real product behavior
```

and:

```text
real Python/data-analysis implementation
```

---

# 52. Definition of Done

CampusLoop is ready when all of the following are true.

## Product

- Home immediately explains the product.
- Discover is useful without explanation.
- A user can inspect an item and understand its sharing option.
- Listings and sharing activities are clearly different.
- Matching provides understandable reasons.
- Impact is based on actual data.

## Data

- All four CSVs are used.
- No fake dataset replaces the supplied data.
- CRUD persists.
- Relationships are validated.
- Missing data is handled.
- Analytics update from current data.

## Academic

- Python is the primary application language.
- Streamlit is the application framework.
- CSV remains persistent storage.
- Pandas is used meaningfully.
- NumPy is used meaningfully where appropriate.
- OOP is visible.
- Exception handling is visible.
- Each student can defend their assigned dataset.
- Required statistics and visualizations exist.
- Reporting exists.

## UI

- The application does not look like default Streamlit.
- Dark visual identity is consistent.
- The poster's character is visible in the design.
- Forms are usable.
- Tables are readable.
- Cards are purposeful.
- Empty/error/success states are designed.
- Responsive behavior works.

## Motion

- Navigation has motion.
- Pages enter cleanly.
- Interactive elements respond.
- CRUD actions have feedback.
- Filters transition cleanly.
- Charts feel integrated.
- Matching has a clear reveal.
- Impact has controlled motion.
- Reduced motion works.

## 3D

- At least one substantial 3D experience exists.
- It supports the product identity.
- It does not obstruct core tasks.
- It has a performance-conscious implementation.
- The application still works if the 3D layer is unavailable.

---

# 53. What Not To Build

Do not add:

- production authentication;
- payment processing;
- real-time chat;
- external campus integrations;
- database migration;
- cloud infrastructure;
- microservices;
- native mobile applications;
- an AI chatbot;
- external AI APIs for matching;
- fake social features;
- fake user activity;
- fake KPI values;
- decorative analytics with no purpose;
- unnecessary gamification;
- a separate frontend application unless a specific Streamlit custom-component requirement justifies it.

Do not expand scope simply because the feature would look impressive in a screenshot.

---

# 54. The Standard

The finished application should pass this test:

### If a student sees it

They should think:

> “I can actually use this to find something on campus.”

### If the evaluator sees it

They should think:

> “This is clearly a Python data-analysis project, and each student understands their implementation.”

### If someone inspects the UI

They should think:

> “This feels like a real product.”

### If someone inspects the motion

They should think:

> “The interface has been designed, not decorated.”

### If someone inspects the 3D

They should think:

> “This gives the product an identity.”

That is the target.

---

# 55. Final Build Rule

Build the smallest system that delivers the full experience above.

Do not build a huge architecture.

Do not build a fake product.

Do not build a pretty prototype with non-functional buttons.

Do not build a correct Python project with an ugly interface.

Build the real workflows first, then make those workflows exceptionally good to use.

```text
REAL DATA
   ↓
REAL WORKFLOW
   ↓
REAL CRUD
   ↓
REAL ANALYTICS
   ↓
REAL PRODUCT UI
   ↓
REAL MOTION
   ↓
REAL 3D
```

The final result should be a coherent CampusLoop product, with the Python implementation visible underneath it.
