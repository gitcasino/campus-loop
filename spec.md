# CampusLoop — Production-Ready Project Specification

> **Course:** 22AIE205 — Introduction to Python  
> **Project Type:** Data Analytics Web Application Development  
> **Technology Choice:** **Option A — Streamlit + Pandas + NumPy + Plotly/Matplotlib**  
> **Theme:** Campus sharing and circular consumption  
> **SDG Alignment:** SDG 12 — Responsible Consumption and Production  
> **Storage:** CSV files only  
> **Primary Goal:** Build a polished, browser-based campus sharing platform where students can borrow, lend, swap, or give away useful items instead of purchasing new ones.

---

## 1. Executive Summary

**CampusLoop** is a Python-based campus sharing platform designed around one simple idea:

> **If another student already has what you need, you should not have to buy it.**

Students can list items they own, discover items available around campus, request or exchange them, and track the measurable impact created by reuse.

Typical items include:

- Calculators
- Textbooks
- Lab equipment
- Chargers and cables
- Electronics
- Stationery
- Clothes
- Bags
- Sports equipment
- Hostel essentials
- Tools
- Event supplies

The application combines:

1. **Full CSV-backed CRUD**
2. **Search, filtering and sorting**
3. **Pandas/NumPy analytics**
4. **Dynamic Plotly/Matplotlib visualizations**
5. **Rule-based smart matching**
6. **Impact tracking**
7. **XP, streaks and leaderboard mechanics**
8. **A premium glassmorphism interface**
9. **Responsive light/dark mode**
10. **Robust validation and exception handling**

The product must feel like a serious modern application while remaining deliberately grounded in the Python concepts required by the course.

---

# 2. Academic Compliance — NON-NEGOTIABLE

The official term-project specification requires a Python web application that manages, analyzes, visualizes and reports on real data stored in CSV files.

The required data flow is:

**Input Data → Update CSV → Read / Analyze / View → Visualize**

Each student must independently own a dataset/CSV and implement:

- Create
- Read
- Update
- Delete
- Visualization

The project must also demonstrate:

- Conditionals
- Loops
- Functions
- Data structures
- File handling
- Exception handling
- OOP
- Modules
- Virtual environment
- Pandas
- NumPy
- Dynamic visualization

The official specification specifically recommends **Streamlit multi-page applications** for Option A and requires every team member to use the same framework. fileciteturn0file0L16-L36

The project therefore **must not replace CSV storage with SQLite, PostgreSQL, MongoDB or another database**.

The application may look production-grade, but its persistence layer remains CSV because CSV is an explicit course requirement.

---

# 3. Project Identity

## Product Name

**CampusLoop**

## Tagline

**Share more. Buy less. Waste less.**

## Product Positioning

CampusLoop is a closed-campus circular economy platform.

Instead of:

> Need item → Buy item → Use briefly → Store/discard item

CampusLoop encourages:

> Need item → Find nearby student → Borrow/swap/receive → Return/reuse → Track impact

---

# 4. Core Product Modules

The application consists of the following major modules.

### 4.1 Home / Campus Overview

Purpose:

- Introduce CampusLoop
- Explain the SDG 12 connection
- Display high-level platform statistics
- Provide navigation to all student-owned modules
- Show recent platform activity if available
- Present the product identity and onboarding information

Possible headline:

> **The campus already has what you need.**

Example metrics:

- Active listings
- Items shared
- Exchanges completed
- Estimated money saved
- Estimated purchases avoided
- Estimated waste avoided
- Active students
- Current sharing streak

The Home page should primarily aggregate/read data and navigate to the individually-owned pages. It must not take ownership of another student's CRUD responsibility.

---

# 5. Student-Owned Dataset Architecture

The course requires every student to own a distinct CSV and a complete vertical slice.

A recommended 4-person team structure is:

| Student Module | CSV | Responsibility |
|---|---|---|
| Student 1 | `listings.csv` | Items available for sharing |
| Student 2 | `users.csv` | Campus member profiles |
| Student 3 | `exchanges.csv` | Borrow/swap/give-away transactions |
| Student 4 | `impact.csv` | Sustainability and economic impact records |

If the team has fewer members, modules may be merged while preserving the rule:

> **Every student owns one dataset and independently implements complete CRUD + analytics + visualization for that dataset.**

The official project specification requires each student's CSV to live inside `/data`, with that student's page responsible for reading/writing its own CSV. fileciteturn0file0L56-L76

---

# 6. Recommended Dataset 1 — Listings

## File

`data/listings.csv`

## Purpose

Represents items currently listed by students for:

- Borrow
- Lend
- Swap
- Give away

## Recommended columns

| Column | Type | Description |
|---|---|---|
| `listing_id` | string | Unique listing identifier |
| `item_name` | string | Human-readable item name |
| `category` | string | Item category |
| `action_type` | string | Borrow / Lend / Swap / Give Away |
| `condition` | string | New / Like New / Good / Fair |
| `owner_id` | string | Student owner identifier |
| `location` | string | Campus/hostel/building location |
| `availability` | string | Available / Reserved / Unavailable |
| `quantity` | int | Available quantity |
| `estimated_value` | float | Approximate replacement value |
| `preferred_duration_days` | int | Preferred borrowing duration |
| `preference_tags` | string | Comma-separated tags |
| `created_date` | string | Listing creation date |
| `updated_date` | string | Last update date |

## CRUD

### Create

Form fields:

- Item name
- Category
- Action type
- Condition
- Owner ID
- Location
- Availability
- Quantity
- Estimated value
- Preferred duration
- Preference tags

Validation:

- Required fields cannot be empty
- Quantity must be positive
- Estimated value cannot be negative
- Duration cannot be negative
- Listing ID must be unique

### Read

Provide:

- Search by item name
- Filter by category
- Filter by action type
- Filter by condition
- Filter by availability
- Filter by location
- Sort by value
- Sort by date
- Sort by condition
- Full table view

### Update

Select by `listing_id`.

Allow editing of:

- Availability
- Quantity
- Location
- Condition
- Estimated value
- Preference tags
- Duration

### Delete

Deletion must require an explicit confirmation step.

Example:

> Are you sure you want to remove **Casio Scientific Calculator**?

Buttons:

- Cancel
- Yes, delete listing

---

# 7. Smart Matching Engine

CampusLoop should include a deterministic rule-based matching engine rather than an external AI dependency.

## Objective

Given a student's request, find the most compatible available listing.

## Input

A request contains:

- Requested item/category
- Preferred action
- Preferred location
- Maximum distance/area tolerance
- Desired condition
- Preferred duration
- Preference tags

## Matching score

Use a transparent weighted scoring model.

Example:

```text
Total Score =
    Category Match        × 35
  + Availability Match    × 20
  + Location Match        × 15
  + Action Match          × 10
  + Condition Match       × 10
  + Duration Match        × 5
  + Preference Match      × 5
```

Maximum:

**100 points**

## Example scoring

### Category

- Exact category: 35
- Related category: 20
- No match: 0

### Availability

- Available: 20
- Reserved: 0
- Unavailable: 0

### Location

- Same location: 15
- Same campus zone: 10
- Different zone: 5

### Action

- Exact requested action: 10
- Compatible action: 5
- Incompatible: 0

### Condition

- Exact requested condition: 10
- Acceptable alternative: 5
- Incompatible: 0

### Duration

- Fully compatible: 5
- Partially compatible: 2
- Incompatible: 0

### Preferences

- Strong tag match: 5
- Partial match: 2
- None: 0

## Output

Display:

- Match score
- Item
- Category
- Owner
- Location
- Condition
- Action
- Estimated value
- Availability
- Why it matched

Example:

> **92% Match**
>
> Casio FX-991ES Plus  
> Same campus zone · Available · Like New  
> Matches category, location, action, condition and duration.

The algorithm must be deterministic and explainable so the student can independently defend it during the final review.

---

# 8. Recommended Dataset 2 — Users

## File

`data/users.csv`

## Purpose

Represents campus members participating in CampusLoop.

## Columns

```text
user_id
name
department
year
campus_zone
hostel
preferred_categories
total_xp
current_streak
items_shared
items_borrowed
items_received
joined_date
status
```

## Analytics

Possible statistics:

- Total users
- Average XP
- Average items shared per user
- Users by department
- Users by year
- Users by campus zone
- Average streak
- Active vs inactive users

## Visualizations

Minimum two dynamic chart types:

1. Users by department — bar chart
2. XP distribution — histogram

Additional:

- Year-wise user distribution
- Campus-zone distribution
- Streak distribution

---

# 9. Recommended Dataset 3 — Exchanges

## File

`data/exchanges.csv`

## Purpose

Represents completed or ongoing sharing activity.

## Columns

```text
exchange_id
listing_id
borrower_id
owner_id
exchange_type
status
requested_date
completed_date
duration_days
estimated_value
location
rating
```

## Exchange types

- Borrow
- Swap
- Give Away

## Status

- Requested
- Approved
- Active
- Completed
- Cancelled

## CRUD

The owner must independently implement:

- Create exchange
- Read/search/filter
- Update status/details
- Delete/cancel record

## Analytics

At least three:

- Total exchanges
- Completed exchanges
- Average exchange duration
- Average estimated value
- Exchanges by type
- Exchanges by status

## Visualizations

Minimum:

1. Exchanges by type — bar/pie
2. Exchanges over time — line chart

---

# 10. Recommended Dataset 4 — Impact

## File

`data/impact.csv`

## Purpose

Tracks measurable outcomes generated through reuse.

## Columns

```text
impact_id
exchange_id
user_id
item_category
estimated_money_saved
estimated_waste_avoided_kg
purchase_avoided
reuse_count
impact_date
```

## Impact model

CampusLoop must clearly label these as **estimated values**, not laboratory measurements.

Example:

```text
Money Saved =
estimated replacement value of item
```

```text
Purchase Avoided =
1 if an exchange replaced a potential purchase
0 otherwise
```

```text
Waste Avoided =
estimated material/waste equivalent associated with avoiding a new purchase
```

The methodology used to calculate these estimates must be visible in the UI.

## Analytics

Minimum:

- Total estimated money saved
- Total estimated waste avoided
- Total purchases avoided
- Average savings per exchange
- Impact by category
- Impact over time

## Visualizations

Minimum:

1. Money saved by category — bar chart
2. Impact over time — line chart

---

# 11. Gamification System

CampusLoop uses lightweight gamification to encourage repeated participation.

## XP

Example rules:

| Action | XP |
|---|---:|
| Create a valid listing | +20 |
| Complete a borrow | +50 |
| Complete a swap | +60 |
| Give away an item | +75 |
| Return an item | +30 |
| Maintain weekly activity | +25 |

XP rules must be centralized in a Python module.

## Streak

A streak increments when a user performs a qualifying sharing activity on consecutive activity periods.

Do not make the algorithm unnecessarily complicated.

## Leaderboard

Display:

- Rank
- Student
- XP
- Items shared
- Exchanges completed
- Current streak

The leaderboard is an informational visualization, not a separate persistence system.

---

# 12. CampusLoop Impact Dashboard

The application should have a dedicated analytics experience.

## KPI cards

Display:

```text
ACTIVE LISTINGS
████████

EXCHANGES
████████

MONEY SAVED
₹██████

WASTE AVOIDED
███ kg

PURCHASES AVOIDED
████

ACTIVE USERS
████
```

## Recommended visualizations

### Chart 1 — Sharing Activity Over Time

Line chart.

X:

`date`

Y:

`exchange count`

### Chart 2 — Items by Category

Bar chart.

### Chart 3 — Estimated Money Saved

Bar chart grouped by category.

### Chart 4 — Sharing Methods

Donut/pie:

- Borrow
- Swap
- Give Away

### Chart 5 — Campus Activity

Bar chart by campus zone.

Charts must always reflect the current CSV state.

---

# 13. Premium UI / UX Specification

The application must feel significantly more polished than a default Streamlit dashboard.

The visual language should communicate:

- Premium
- Modern
- Trustworthy
- Sustainable
- Academic
- Technology-focused

## Design Direction

**Luxury glassmorphism + modern campus technology.**

Avoid:

- Generic Streamlit appearance
- Excessive gradients
- Cartoonish sustainability imagery
- Huge unnecessary animations
- Cluttered dashboards
- Overly bright neon colors

---

# 14. Theme System

Provide a visible mode switch.

## Dark Mode

Primary environment:

- Near-black background
- Deep charcoal surfaces
- Frosted glass panels
- Soft borders
- High-contrast white typography
- Emerald/teal sustainability accent
- Subtle gold accent for premium details

## Light Mode

- Warm off-white background
- White glass panels
- Dark charcoal typography
- Emerald/teal primary accent
- Soft neutral borders
- Reduced shadow intensity

The selected mode should persist during the session using Streamlit session state.

Example conceptual state:

```python
st.session_state["theme"] = "dark"
```

Do not create a second storage system just for theme preferences.

---

# 15. Glassmorphism System

Reusable visual classes/styles should be established centrally.

Conceptual design:

```css
.glass-panel {
    backdrop-filter: blur(18px);
    border: 1px solid rgba(...);
    border-radius: 20px;
    box-shadow: 0 12px 40px rgba(...);
}
```

Components should visually use:

- Glass cards
- Glass navigation
- Glass metric panels
- Glass filters
- Glass forms
- Glass tables where practical

Keep text readable.

Accessibility takes priority over visual effects.

---

# 16. Navigation

Recommended navigation:

```text
CampusLoop
│
├── Home
├── Discover
├── My Listings
├── Exchanges
├── Impact
├── Leaderboard
└── About
```

However, because the course requires each student's dataset to have its own page, the actual `/pages` structure must preserve individual ownership.

Example:

```text
Home.py
pages/
├── 1_Listings.py
├── 2_Users.py
├── 3_Exchanges.py
└── 4_Impact.py
```

The page numbering can be adjusted to match the actual team members.

The official submission structure requires `app.py`/`Home.py`, a `/pages` directory with one page per student, and a `/data` directory containing the student-owned CSV files. fileciteturn0file0L156-L170

---

# 17. Component System

Create reusable Python UI/helper modules rather than duplicating large blocks of code.

Recommended:

```text
src/
├── ui/
│   ├── theme.py
│   ├── components.py
│   ├── cards.py
│   ├── navigation.py
│   └── styles.py
```

Possible reusable components:

- `metric_card()`
- `section_header()`
- `status_badge()`
- `empty_state()`
- `error_message()`
- `success_message()`
- `glass_panel()`
- `render_dataframe()`
- `render_chart()`

The course is specifically testing modular Python development, so these helpers should remain understandable and defensible.

---

# 18. Recommended Project Structure

```text
campus-loop/
│
├── Home.py
├── README.md
├── requirements.txt
├── .gitignore
├── specs.md
│
├── pages/
│   ├── 1_Listings.py
│   ├── 2_Users.py
│   ├── 3_Exchanges.py
│   └── 4_Impact.py
│
├── data/
│   ├── listings.csv
│   ├── users.csv
│   ├── exchanges.csv
│   └── impact.csv
│
├── core/
│   ├── __init__.py
│   ├── csv_manager.py
│   ├── validators.py
│   ├── matching.py
│   ├── analytics.py
│   ├── impact.py
│   └── gamification.py
│
├── models/
│   ├── __init__.py
│   ├── listing.py
│   ├── user.py
│   ├── exchange.py
│   └── impact_record.py
│
├── ui/
│   ├── __init__.py
│   ├── theme.py
│   ├── styles.py
│   ├── components.py
│   └── charts.py
│
├── reports/
│   └── .gitkeep
│
└── assets/
    └── .gitkeep
```

If the team wants a simpler structure, `core/`, `models/`, and `ui/` may be reduced. Do not introduce unnecessary architecture merely for appearance.

---

# 19. OOP Architecture

The project must demonstrate meaningful OOP.

## Shared base class

Recommended:

```python
class CSVManager:
    def __init__(self, file_path, required_columns):
        ...

    def load(self):
        ...

    def save(self, dataframe):
        ...

    def validate(self, dataframe):
        ...
```

Then student-specific classes can extend it.

Example:

```python
class ListingManager(CSVManager):
    def create_listing(self, record):
        ...

    def get_listings(self, filters=None):
        ...

    def update_listing(self, listing_id, updates):
        ...

    def delete_listing(self, listing_id):
        ...
```

This provides the required demonstration of shared encapsulation/inheritance.

The official specification requires at least one custom class per student's dataset and requires the team to demonstrate inheritance or encapsulation somewhere in the combined codebase. fileciteturn0file0L94-L100

---

# 20. CSV Safety Architecture

CSV persistence is a core grading requirement.

Every CSV operation must be robust.

## Read flow

```text
Request
  ↓
Validate file path
  ↓
try:
    read CSV
except FileNotFoundError:
    show friendly message
except EmptyDataError:
    show empty-state message
except parser/type error:
    show data error
else:
    validate structure
finally:
    finish operation safely
```

## Write flow

Never directly overwrite the production CSV if the operation can leave it partially written.

Preferred:

```text
DataFrame
   ↓
Validate
   ↓
Write temporary CSV
   ↓
Replace original
```

This protects against corrupted writes.

The official specification explicitly requires every write to leave the CSV valid and reloadable, recommending a temporary-file-and-replace strategy or another safe mechanism. fileciteturn0file0L88-L100

---

# 21. Mandatory Error Handling

The application must never expose raw tracebacks to the user.

Handle explicitly:

### Missing file

Display:

> Listings data could not be loaded. The CSV file may be missing.

### Empty file

Display:

> No records are available yet. Create the first listing to get started.

### Wrong column types

Display:

> Some records contain invalid data. Please check the highlighted fields.

### Invalid record ID

Display:

> Listing `L-1042` was not found.

### Duplicate ID

Display:

> A listing with this ID already exists.

### Invalid numeric value

Display:

> Estimated value must be a non-negative number.

### Invalid quantity

Display:

> Quantity must be greater than zero.

### Invalid form submission

Display the problem beside the relevant field wherever possible.

---

# 22. Validation Layer

Create centralized validation functions.

Examples:

```python
validate_required(value)
validate_positive_integer(value)
validate_non_negative_number(value)
validate_unique_id(dataframe, record_id)
validate_category(category)
validate_action_type(action_type)
validate_date(date_value)
```

Validation should occur **before** modifying the CSV.

---

# 23. Missing Data Policy

Missing data must be handled explicitly.

Recommended policy:

- Required identifiers: reject missing values
- Required categorical fields: reject missing values
- Optional descriptive fields: allow missing values
- Numeric analytics: exclude invalid/missing records where appropriate
- UI: clearly indicate how missing values were treated

The interface should include a small note such as:

> **Data note:** Missing optional values are excluded from numerical aggregation.

The course specification explicitly requires missing/NaN data to be handled explicitly and the chosen treatment to be stated in the UI. fileciteturn0file0L101-L107

---

# 24. Analytics Requirements

Every student page must calculate at least **three summary statistics** using Pandas/NumPy.

Do not fake statistics.

Examples:

```python
df["estimated_value"].mean()
df["category"].value_counts()
df.groupby("condition")["estimated_value"].mean()
```

Possible metrics:

- Count
- Mean
- Median
- Sum
- Minimum
- Maximum
- Group-by totals
- Standard deviation
- Unique count

At least three should be visible and connected to the student's dataset.

The official specification requires at least three summary statistics per student and at least two dynamic chart types. fileciteturn0file0L101-L106

---

# 25. Visualization Requirements

Each student-owned page must have at least **two different chart types**.

Recommended CampusLoop chart vocabulary:

### Bar chart

Good for:

- Categories
- Departments
- Exchange types
- Locations

### Line chart

Good for:

- Activity over time
- Impact over time
- Listings created over time

### Histogram

Good for:

- Item value
- XP
- Exchange duration

### Pie / Donut

Good for:

- Action type
- Exchange status

Charts must be dynamically generated from the current CSV.

No hardcoded chart images.

---

# 26. Filtering Architecture

Every major dataset page should provide filters before analytics.

Example Listings filters:

```text
Search item        [________________]

Category           [All ▼]
Action             [All ▼]
Condition          [All ▼]
Availability       [Available ▼]
Location           [All ▼]

[Clear Filters]
```

The filtered DataFrame becomes the source for:

- Table
- Summary metrics
- Charts
- Exported report

This makes the application demonstrably dynamic.

---

# 27. Reporting

Every student page must provide an exportable summary report.

Acceptable formats from the course specification:

- CSV
- PDF
- Plain text

Recommended initial implementation:

**CSV + TXT**

Optional:

**PDF**

Every report must include:

- Timestamp
- Dataset name
- Current row count
- Active filters
- Summary statistics
- Relevant analysis

Example:

```text
CampusLoop — Listings Report
Generated: 2026-10-01 14:32:10

Rows: 84

Filters:
Category: Electronics
Availability: Available

Statistics:
Average estimated value: ₹1,240
Median estimated value: ₹900
Available listings: 71
```

The official specification requires the summary report to contain a timestamp, row count and applied filters. fileciteturn0file0L109-L111

---

# 28. Home Page Experience

The landing page should immediately communicate what CampusLoop does.

## Hero

```text
CAMPUSLOOP

Share more.
Buy less.
Waste less.

A student-powered circular economy for campus.

[Explore Items]   [List an Item]
```

## Hero supporting text

> Find what you need, share what you no longer use, and turn everyday campus exchanges into measurable impact.

## KPI strip

```text
1,284
Items Shared

₹2.84L
Estimated Savings

412 kg
Waste Avoided

736
Purchases Avoided
```

Values must come from the actual current datasets, not hardcoded marketing numbers once real data is available.

---

# 29. Discover Experience

The Discover interface should prioritize practical usefulness.

Each item can be represented as a premium card:

```text
┌────────────────────────────────────┐
│  CASIO FX-991ES PLUS        94%    │
│  ────────────────────────────────  │
│  Electronics · Like New            │
│                                    │
│  📍 Main Block                     │
│  ↔ Borrow                          │
│                                    │
│  ₹1,250 estimated value            │
│                                    │
│  [View Match]                      │
└────────────────────────────────────┘
```

The score should be generated by the matching engine.

---

# 30. Empty States

Empty pages should feel intentional.

Example:

> **Nothing here yet.**
>
> Your campus loop starts with one item.
>
> `[Create Listing]`

Do not display blank tables without explanation.

---

# 31. Loading and Interaction States

Avoid unnecessary fake loading animations.

Use Streamlit's native execution model and lightweight visual feedback:

- Success messages
- Progress indicators when genuinely useful
- Spinner for expensive operations
- Disabled controls where appropriate

---

# 32. Accessibility

The premium UI must remain usable.

Requirements:

- Sufficient text/background contrast
- Clear form labels
- No information conveyed only by color
- Meaningful button labels
- Readable chart titles
- Mobile-friendly layout where Streamlit permits it
- Avoid excessive animation
- Keep important actions obvious

---

# 33. Dependencies

Minimum expected stack:

```text
streamlit
pandas
numpy
plotly
matplotlib
```

Optional packages should only be added when genuinely required.

Every dependency must be included in:

```text
requirements.txt
```

The official specification requires Python 3.10+ and explicitly states that every dependency must be listed because evaluation will use a clean environment with `pip install -r requirements.txt`. fileciteturn0file0L40-L55

Recommended target:

```text
Python 3.10+
```

Prefer a currently supported Python version compatible with the selected Streamlit/Pandas/NumPy stack.

---

# 34. No External Backend Requirement

CampusLoop should **not** require:

- MongoDB
- PostgreSQL
- Firebase
- Supabase
- Redis
- Docker
- External authentication
- Paid APIs

The project must remain easy to run during evaluation.

The core application should work completely offline after dependencies are installed.

---

# 35. Authentication

Authentication is **not a core academic requirement**.

If simulated identity is desired, use a simple session-state user selector:

```text
Current Student
[ Rahul ▼ ]
```

Do not introduce a real authentication backend unless there is a clear reason.

This keeps the application focused on the course requirements.

---

# 36. Data Generation

The project should ship with a realistic seed dataset so the application looks functional immediately.

Generate enough records for meaningful analytics.

Suggested minimum:

```text
Listings: 80–150
Users: 30–60
Exchanges: 60–120
Impact records: 60–120
```

The seed data should contain:

- Multiple categories
- Multiple locations
- Multiple conditions
- Multiple action types
- Different dates
- Different values
- A small amount of controlled missing optional data
- Realistic distributions

Avoid fake-looking random strings.

Example:

```text
item_name:
Casio FX-991ES Plus
Engineering Mathematics Vol. 2
USB-C 65W Charger
Lab Coat
Arduino Uno
Scientific Calculator
Mechanical Keyboard
Football
Graph Paper Bundle
```

---

# 37. Data Integrity Rules

Each dataset must have a unique primary identifier.

Examples:

```text
L-0001
U-0001
E-0001
I-0001
```

Rules:

- IDs cannot be duplicated
- IDs cannot be empty
- Deleted records must disappear from the CSV
- Updates must persist after refresh
- Create operations must persist after refresh
- CSV must remain valid after every write
- Dates must use one consistent format
- Numeric fields must remain numeric

---

# 38. Academic Review / Defensibility

The final product must not be so abstract that the student cannot explain it.

Every student should be able to explain:

### Python fundamentals

- Lists
- Dictionaries
- Tuples
- Loops
- Conditionals
- Functions

### File handling

- Opening/reading CSV
- Writing CSV
- Exception handling
- Safe file replacement

### OOP

- Their custom class
- Constructor
- Methods
- Encapsulation/inheritance where applicable

### Pandas

- DataFrame
- Filtering
- Group-by
- Aggregation
- Missing data

### NumPy

- Numerical aggregation or calculations

### Visualization

- Why their chart types fit their data
- How charts update when CSV data changes

### Application logic

- CRUD lifecycle
- Validation
- Duplicate detection
- Matching algorithm
- Report generation

The official project requires every student to independently present and defend their own page during the live final review. fileciteturn0file0L142-L155

---

# 39. Demo Flow

The 10–15 minute demonstration should feel like a product demo rather than a code dump.

Recommended sequence:

## 1. Product introduction — 45 seconds

Explain:

> CampusLoop turns unused campus resources into a reusable student-to-student sharing network.

## 2. Home — 1 minute

Show:

- Branding
- Theme switch
- KPIs
- SDG connection

## 3. Create — 1–2 minutes

Create a real listing.

Show:

- Validation
- Successful CSV persistence

## 4. Read / Filter — 1 minute

Search and filter records.

## 5. Update — 1 minute

Modify a listing.

Refresh/read the CSV state.

## 6. Delete — 1 minute

Delete a test record with confirmation.

## 7. Analytics — 2 minutes

Show:

- Statistics
- Dynamic charts
- Filter-dependent visualization

## 8. Smart Matching — 1–2 minutes

Enter a request and show ranked matches with explanations.

## 9. Impact — 1 minute

Show:

- Savings
- Waste avoided
- Purchases avoided
- Sharing activity

## 10. Reporting — 30 seconds

Generate/export the report.

## 11. Code ownership — 1 minute

Open the student's class and explain the CRUD methods.

---

# 40. Testing Strategy

At minimum, test:

## CRUD

- Create valid record
- Create duplicate
- Read existing data
- Update valid ID
- Update invalid ID
- Delete valid ID
- Delete invalid ID
- Cancel deletion

## Validation

- Empty required field
- Invalid number
- Negative number
- Invalid category
- Duplicate ID

## File failures

- Missing CSV
- Empty CSV
- Malformed CSV
- Wrong data type

## Analytics

- Empty filtered dataset
- Single-row dataset
- Missing optional values
- Multiple categories

## Matching

- Exact match
- Partial match
- No available items
- Multiple equal-score candidates

---

# 41. Performance Principles

This is a small academic application, so optimize for:

**correctness → clarity → maintainability → visual polish → performance**

Do not build unnecessary distributed architecture.

For CSV datasets of the expected project size:

- Loading a DataFrame per page is acceptable
- Pandas filtering is sufficient
- Plotly is sufficient
- No database cache is necessary

---

# 42. Security / Safety Basics

Even though this is a local academic application:

- Never use `eval()` on user input
- Never execute user-provided Python
- Validate all numeric input
- Restrict file operations to known `/data` paths
- Do not accept arbitrary file paths from users
- Do not store secrets in CSV
- Do not commit `.env` files containing secrets
- Do not hardcode absolute local paths

The official submission must use relative paths from the project root rather than hardcoded machine-specific paths. fileciteturn0file0L156-L170

---

# 43. Git / Repository Standards

Recommended repository:

```text
campus-loop/
```

Recommended commits:

```text
feat: initialize streamlit architecture
feat: add listings dataset and CRUD
feat: add users dataset and analytics
feat: add exchanges module
feat: add impact analytics
feat: add smart matching engine
feat: add premium glass UI
feat: add theme switching
feat: add reporting
fix: harden csv persistence
docs: add setup and project documentation
```

Avoid committing:

```text
.venv/
__pycache__/
*.pyc
.env
.DS_Store
```

---

# 44. README Requirements

`README.md` must contain:

## Project Overview

What CampusLoop is.

## SDG Connection

How it supports SDG 12.

## Features

- CRUD
- Matching
- Analytics
- Visualization
- Impact tracking
- Gamification
- Reporting

## Technology

```text
Python
Streamlit
Pandas
NumPy
Plotly
Matplotlib
CSV
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows equivalent should also be documented.

## Run

```bash
streamlit run Home.py
```

## Dataset Ownership

Include a table:

| Student | Dataset | Page | Class |
|---|---|---|---|
| Student 1 | listings.csv | Listings | ListingManager |
| Student 2 | users.csv | Users | UserManager |
| Student 3 | exchanges.csv | Exchanges | ExchangeManager |
| Student 4 | impact.csv | Impact | ImpactManager |

Replace placeholder names with actual team members.

## Screenshots / Demo

Include screenshots or demo video link.

The official submission guidelines explicitly require setup/run instructions and a table identifying which student owns which CSV/page. fileciteturn0file0L156-L168

---

# 45. Definition of Done — Academic

A student's module is complete only when all are true:

- [ ] Own CSV exists in `/data`
- [ ] Own page exists in `/pages`
- [ ] Custom class implemented
- [ ] Create implemented
- [ ] Read implemented
- [ ] Update implemented
- [ ] Delete implemented
- [ ] Duplicate detection implemented
- [ ] Invalid ID handled
- [ ] Missing file handled
- [ ] Empty file handled
- [ ] Wrong data type handled
- [ ] Every CSV read/write safely wrapped
- [ ] At least 3 statistics
- [ ] At least 2 chart types
- [ ] Charts respond to current CSV/filter state
- [ ] Missing data policy displayed
- [ ] Exportable report
- [ ] Timestamp in report
- [ ] Row count in report
- [ ] Filters in report
- [ ] No raw traceback shown to user
- [ ] Fresh environment installation works

---

# 46. Definition of Done — Product

CampusLoop is considered product-complete when:

- [ ] Home page communicates the concept within 10 seconds
- [ ] Navigation is consistent
- [ ] Dark/light mode works
- [ ] Glass UI is consistent
- [ ] Forms are polished
- [ ] Tables are readable
- [ ] Empty states exist
- [ ] Errors are human-readable
- [ ] Smart matching is explainable
- [ ] Impact numbers are clearly marked as estimates
- [ ] Dashboard updates from CSV state
- [ ] No hardcoded analytics values remain
- [ ] Seed data is realistic
- [ ] Demo can be completed without external services
- [ ] Application survives invalid user input
- [ ] Application runs after clean dependency installation

---

# 47. Scope Guardrails

## Must Have

1. CSV persistence
2. Full CRUD
3. OOP
4. Pandas
5. NumPy
6. Dynamic charts
7. Search/filter/sort
8. Exception handling
9. Reports
10. Premium UI
11. Light/dark mode
12. Smart matching
13. Impact analytics

## Should Have

1. XP
2. Streaks
3. Leaderboard
4. Animated KPI transitions
5. Rich empty states
6. Advanced filtering
7. Match explanations

## Nice to Have

1. PDF reports
2. Confetti/success animation
3. Animated hero background
4. Item recommendation carousel
5. Advanced impact projections

## Explicitly Avoid

- Database migration
- Real authentication backend
- Payment system
- Real-time messaging
- External AI APIs
- Complex microservices
- Docker dependency
- Cloud infrastructure
- Unnecessary third-party services

These features may look impressive but create evaluation risk and distract from the required Python/CSV learning objectives.

---

# 48. Product Principles

### Principle 1 — CSV First

Every important persistent state must ultimately be represented in CSV.

### Principle 2 — Explainable Intelligence

The matching algorithm must be understandable without an AI API.

### Principle 3 — Dynamic, Never Fake

Charts and metrics must come from the current dataset.

### Principle 4 — Every Student Owns a Vertical Slice

No student should only contribute UI or helper code.

### Principle 5 — Graceful Failure

Bad input should produce a useful message, never a traceback.

### Principle 6 — Premium Without Overengineering

The interface can look like a high-end product while the underlying architecture remains simple enough for an Introduction to Python course.

### Principle 7 — Defend Every Line

If a feature cannot be explained during the final review, it does not belong in the core implementation.

---

# 49. Final Product Vision

CampusLoop should feel like a real product:

> A student needs a calculator for tomorrow's exam.
>
> Instead of opening an e-commerce app and buying one, they open CampusLoop.
>
> They enter:
>
> **Scientific calculator · Tomorrow · Main Block**
>
> CampusLoop searches the available campus inventory.
>
> It finds:
>
> **Casio FX-991ES Plus — 94% match**
>
> The student borrows it.
>
> The owner earns XP.
>
> The borrower avoids a purchase.
>
> The platform records estimated money saved.
>
> The impact dashboard updates.
>
> One item gets reused instead of another item being purchased.

That is the central product loop:

```text
LIST
  ↓
DISCOVER
  ↓
MATCH
  ↓
SHARE
  ↓
REUSE
  ↓
MEASURE IMPACT
  ↓
EARN XP
  ↓
SHARE AGAIN
```

---

# 50. Final Architecture

```text
                         ┌──────────────────────┐
                         │      CampusLoop      │
                         │     Streamlit UI     │
                         └──────────┬───────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
        ┌─────▼─────┐        ┌──────▼──────┐       ┌─────▼─────┐
        │   Pages   │        │ UI / Theme  │       │ Analytics │
        │ CRUD      │        │ Glass / Mode│       │ Pandas/NP │
        └─────┬─────┘        └─────────────┘       └─────┬─────┘
              │                                          │
              └──────────────────┬───────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │       Core Logic        │
                    │                         │
                    │ CSV Manager             │
                    │ Validation              │
                    │ Matching                │
                    │ Impact                  │
                    │ Gamification            │
                    └────────────┬────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
        ┌─────▼─────┐      ┌─────▼─────┐      ┌────▼──────┐
        │ listings  │      │   users   │      │ exchanges │
        │   .csv    │      │   .csv    │      │   .csv    │
        └───────────┘      └───────────┘      └───────────┘
                                 │
                          ┌──────▼──────┐
                          │   impact    │
                          │    .csv     │
                          └─────────────┘
```

---

# 51. Submission Checklist

Before the hard deadline:

**22 October — 10:00 AM**

verify:

```text
[ ] GitHub repository works
[ ] ZIP opens correctly
[ ] requirements.txt is complete
[ ] Clean virtual environment tested
[ ] Home.py runs
[ ] Every page runs
[ ] Every CSV exists
[ ] CRUD works
[ ] Charts work
[ ] Reports work
[ ] Error handling works
[ ] No absolute paths
[ ] No secrets committed
[ ] README complete
[ ] Dataset ownership table complete
[ ] Screenshots/demo ready
[ ] Each student can explain their own code
[ ] 10–15 minute demo rehearsed
```

The official specification sets **22 October at 10:00 AM** as the hard submission deadline and states that late submissions are not accepted. The evaluation includes the demo, an individual quiz targeting the student's own dataset/page, and an individual live code walkthrough. fileciteturn0file0L118-L155

---

# 52. Success Criteria

CampusLoop succeeds if it simultaneously satisfies three layers:

## Layer 1 — Academic Correctness

The evaluator can clearly see:

```text
Python
↓
OOP
↓
CSV
↓
CRUD
↓
Pandas / NumPy
↓
Visualization
↓
Exception Handling
```

## Layer 2 — Product Quality

A user can naturally:

```text
Find → Match → Share → Reuse → Track Impact
```

without confusion.

## Layer 3 — Visual Quality

The application feels:

```text
Premium
Modern
Consistent
Responsive
Purposeful
```

without sacrificing the simplicity required for a Python course project.

---

# FINAL DIRECTIVE

Build **CampusLoop** as a polished, self-contained Streamlit application whose visual quality resembles a premium modern SaaS product, while keeping the underlying implementation transparent enough for an Introduction to Python final review.

The application must prioritize:

**correct CSV persistence → complete CRUD → robust Python/OOP → real Pandas/NumPy analytics → dynamic visualization → explainable matching → polished UI.**

Do not sacrifice the academic requirements for unnecessary production infrastructure.

**CampusLoop is not a database project with a pretty frontend.**

It is a **Python data analytics application presented as a premium campus circular-economy product.**
