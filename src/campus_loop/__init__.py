"""CampusLoop core modules and data managers."""

import os
import tempfile
from typing import Any, Dict, List, Optional

import pandas as pd
import numpy as np


PALETTE = {
    "background": "#050A0A",
    "surface": "#0B1415",
    "primary_green": "#8CFF66",
    "secondary_green": "#38D996",
    "soft_green": "#B8FF9A",
    "text": "#F4F7F5",
    "muted": "#9AA7A0",
    "gold": "#D6A84F",
}


class CSVManager:
    """Base manager for CSV file operations with robust error handling."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self._df: Optional[pd.DataFrame] = None

    def _read_file(self) -> pd.DataFrame:
        """Read CSV file, handling missing/empty/malformed data."""
        if not os.path.exists(self.filepath):
            return pd.DataFrame(columns=self._get_columns())
        try:
            df = pd.read_csv(self.filepath)
            if df.empty:
                return pd.DataFrame(columns=self._get_columns())
            return df
        except (pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeDecodeError):
            return pd.DataFrame(columns=self._get_columns())

    def _get_columns(self) -> List[str]:
        """Return the expected column names for this CSV."""
        return []

    def load(self) -> pd.DataFrame:
        """Load CSV data into DataFrame."""
        self._df = self._read_file()
        return self._df

    def save(self, df: pd.DataFrame) -> None:
        """Save DataFrame to CSV atomically using temp file replacement."""
        if df.empty:
            df = pd.DataFrame(columns=self._get_columns())
        dir_name = os.path.dirname(self.filepath) or "."
        try:
            fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix=".csv")
            with os.fdopen(fd, "w", newline="") as f:
                df.to_csv(f, index=False)
            os.replace(tmp_path, self.filepath)
        except Exception:
            # If save fails, try direct write as fallback
            try:
                df.to_csv(self.filepath, index=False)
            except Exception:
                pass

    def get(self, item_id: str) -> Optional[pd.DataFrame]:
        """Get a single record by ID."""
        df = self.load()
        if df.empty:
            return None
        result = df[df["item_id"] == item_id] if "item_id" in df.columns else df[df.iloc[:, 0] == item_id]
        if result.empty:
            return None
        return result

    def filter(self, **kwargs) -> pd.DataFrame:
        """Filter records by column values."""
        df = self.load()
        if df.empty:
            return df
        result = df
        for col, val in kwargs.items():
            if col in result.columns:
                result = result[result[col] == val]
        return result

    def count(self) -> int:
        """Return number of records."""
        return len(self.load())

    def unique(self, column: str) -> List[Any]:
        """Return unique values for a column."""
        df = self.load()
        if column not in df.columns:
            return []
        return df[column].dropna().unique().tolist()

    def get_new_id(self) -> str:
        """Generate the next ID in sequence."""
        df = self.load()
        if df.empty:
            return self._get_default_id("0001")
        existing_ids = df.iloc[:, 0].tolist()
        try:
            last_num = max(int(str(x).lstrip("I")) for x in existing_ids if str(x).startswith("I"))
            return self._get_default_id(str(last_num + 1).zfill(4))
        except (ValueError, TypeError):
            return self._get_default_id("5001")

    @staticmethod
    def _get_default_id(s: str) -> str:
        return f"I{s}" if s.startswith("0") and "item" in str.lower else f"A{s}" if not s.startswith("I") else s


class ItemListingManager(CSVManager):
    """Manager for item_listings.csv — Rahul's owned dataset."""

    def _get_columns(self) -> List[str]:
        return [
            "item_id", "owner_user_id", "title", "category", "item_type",
            "brand", "condition", "sharing_mode", "status",
            "estimated_value_inr", "listed_date", "available_until", "pickup_location"
        ]

    def add(
        self,
        owner_user_id: str,
        title: str,
        category: str,
        item_type: str,
        brand: str,
        condition: str,
        sharing_mode: str,
        status: str = "AVAILABLE",
        estimated_value_inr: int = 0,
        listed_date: Optional[str] = None,
        available_until: Optional[str] = None,
        pickup_location: str = "",
    ) -> pd.DataFrame:
        """Add a new item listing."""
        df = self.load()
        new_id = self.get_new_id()
        listed_date = listed_date or pd.Timestamp.now().strftime("%Y-%m-%d")
        available_until = available_until or (pd.Timestamp.now() + pd.Timedelta(days=90)).strftime("%Y-%m-%d")

        new_row = {
            "item_id": new_id,
            "owner_user_id": owner_user_id,
            "title": title,
            "category": category,
            "item_type": item_type,
            "brand": brand,
            "condition": condition,
            "sharing_mode": sharing_mode,
            "status": status,
            "estimated_value_inr": estimated_value_inr,
            "listed_date": listed_date,
            "available_until": available_until,
            "pickup_location": pickup_location,
        }

        # Prepend ID column at position 0 if needed
        df_with_id = pd.DataFrame([new_row])
        if df.empty:
            df = df_with_id
        else:
            # Ensure item_id is first column
            cols = self._get_columns()
            new_order = ["item_id"] + [c for c in cols if c != "item_id"]
            df_with_id = df_with_id[new_order]
            df = pd.concat([df_with_id, df], ignore_index=True)

        self.save(df)
        return df

    def update(
        self,
        item_id: str,
        updates: Dict[str, Any],
    ) -> pd.DataFrame:
        """Update an existing item listing."""
        df = self.load()
        mask = df["item_id"] == item_id
        if not mask.any():
            raise ValueError(f"Item listing {item_id} not found")
        for key, val in updates.items():
            if key in df.columns:
                df.loc[mask, key] = val
        self.save(df)
        return df

    def delete(self, item_id: str) -> pd.DataFrame:
        """Delete an item listing."""
        df = self.load()
        mask = df["item_id"] == item_id
        if not mask.any():
            raise ValueError(f"Item listing {item_id} not found")
        df = df[~mask]
        self.save(df)
        return df

    def search(
        self,
        query: str = "",
        category: str = "",
        sharing_mode: str = "",
        condition: str = "",
    ) -> pd.DataFrame:
        """Search and filter item listings."""
        df = self.load()
        if df.empty:
            return df

        result = df.copy()
        if query:
            result = result[result["title"].str.contains(query, case=False, na=False) | result["category"].str.contains(query, case=False, na=False)]
        if category:
            result = result[result["category"] == category]
        if sharing_mode:
            result = result[result["sharing_mode"] == sharing_mode]
        if condition:
            result = result[result["condition"] == condition]
        return result.sort_values("item_id").reset_index(drop=True)


class SharingActivityManager(CSVManager):
    """Manager for sharing_activities.csv — Rahul's owned dataset."""

    def _get_columns(self) -> List[str]:
        return [
            "activity_id", "item_id", "borrower_user_id", "owner_user_id",
            "activity_type", "start_date", "request_date", "due_date",
            "activity_status", "duration_days", "estimated_value_inr",
            "resolution_status", "return_status"
        ]

    def add(
        self,
        item_id: str,
        borrower_user_id: str,
        owner_user_id: str,
        activity_type: str,
        start_date: str,
        request_date: str,
        due_date: str,
        activity_status: str = "ACTIVE",
        duration_days: int = 0,
        estimated_value_inr: int = 0,
        resolution_status: str = "PENDING",
        return_status: str = "NA",
    ) -> pd.DataFrame:
        """Add a new sharing activity."""
        df = self.load()
        new_id = self._generate_activity_id(df)
        new_row = {
            "activity_id": new_id,
            "item_id": item_id,
            "borrower_user_id": borrower_user_id,
            "owner_user_id": owner_user_id,
            "activity_type": activity_type,
            "start_date": start_date,
            "request_date": request_date,
            "due_date": due_date,
            "activity_status": activity_status,
            "duration_days": duration_days,
            "estimated_value_inr": estimated_value_inr,
            "resolution_status": resolution_status,
            "return_status": return_status,
        }
        new_df = pd.DataFrame([new_row])
        cols = self._get_columns()
        new_df = new_df[cols]
        df = pd.concat([new_df, df], ignore_index=True)
        self.save(df)
        return df

    def _generate_activity_id(self, df: pd.DataFrame) -> str:
        """Generate the next activity ID."""
        if df.empty:
            return "A000001"
        existing_ids = df["activity_id"].tolist()
        try:
            last_num = max(int(str(x).lstrip("A")) for x in existing_ids if str(x).startswith("A"))
            return f"A{str(last_num + 1).zfill(6)}"
        except (ValueError, TypeError):
            return f"A{str(int('000001') + 1).zfill(6)}"

    def update(
        self,
        activity_id: str,
        updates: Dict[str, Any],
    ) -> pd.DataFrame:
        """Update a sharing activity."""
        df = self.load()
        mask = df["activity_id"] == activity_id
        if not mask.any():
            raise ValueError(f"Sharing activity {activity_id} not found")
        for key, val in updates.items():
            if key in df.columns:
                df.loc[mask, key] = val
        self.save(df)
        return df

    def delete(self, activity_id: str) -> pd.DataFrame:
        """Delete a sharing activity."""
        df = self.load()
        mask = df["activity_id"] == activity_id
        if not mask.any():
            raise ValueError(f"Sharing activity {activity_id} not found")
        df = df[~mask]
        self.save(df)
        return df

    def get_active_borrows(self, user_id: str) -> pd.DataFrame:
        """Get active borrows for a user."""
        df = self.load()
        if df.empty:
            return df
        return df[
            (df["borrower_user_id"] == user_id) &
            (df["activity_status"] == "ACTIVE")
        ].sort_values("start_date", ascending=False)

    def get_by_item(self, item_id: str) -> pd.DataFrame:
        """Get activities for a specific item."""
        df = self.load()
        if df.empty:
            return df
        return df[df["item_id"] == item_id].sort_values("start_date", ascending=False)


class UserManager:
    """Read-only manager for users.csv (owned by another teammate)."""

    def __init__(self, filepath: str = "data/users.csv"):
        self.filepath = filepath

    def load(self) -> pd.DataFrame:
        """Load users CSV."""
        manager = CSVManager(self.filepath)
        manager._columns = self._get_columns()
        return manager.load()

    def _get_columns(self) -> List[str]:
        return ["user_id", "name", "email", "department", "year", "joined_date", "account_status"]

    def get(self, user_id: str) -> Optional[pd.DataFrame]:
        """Get a single user by ID."""
        df = self.load()
        if df.empty:
            return None
        result = df[df["user_id"] == user_id]
        if result.empty:
            return None
        return result

    def filter_by_department(self, department: str) -> pd.DataFrame:
        """Filter users by department."""
        df = self.load()
        if df.empty:
            return df
        return df[df["department"] == department]


class ImpactManager:
    """Read-only manager for impact.csv (owned by another teammate)."""

    def __init__(self, filepath: str = "data/impact.csv"):
        self.filepath = filepath

    def load(self) -> pd.DataFrame:
        """Load impact CSV."""
        manager = CSVManager(self.filepath)
        manager._columns = self._get_columns()
        return manager.load()

    def _get_columns(self) -> List[str]:
        return [
            "impact_id", "activity_id", "user_id", "activity_type",
            "impact_date", "items_reused", "duration_days",
            "estimated_value_saved_inr", "estimated_material_reuse_factor",
            "item_category", "impact_category"
        ]

    def get_summary(self) -> Dict[str, Any]:
        """Get impact summary statistics."""
        df = self.load()
        if df.empty:
            return {"total_impact": 0, "total_value_saved": 0, "total_items_reused": 0, "average_reuse_factor": 0}
        total_impact = len(df)
        total_value_saved = df["estimated_value_saved_inr"].sum()
        total_items_reused = df["items_reused"].sum()
        avg_reuse_factor = df["estimated_material_reuse_factor"].mean()
        return {
            "total_impact": int(total_impact),
            "total_value_saved": float(total_value_saved),
            "total_items_reused": int(total_items_reused),
            "average_reuse_factor": float(round(avg_reuse_factor, 2)),
        }

    def get_by_category(self) -> pd.DataFrame:
        """Get impact breakdown by category."""
        df = self.load()
        if df.empty:
            return df
        return df.groupby("item_category").agg(
            count=("impact_id", "count"),
            total_value_saved=("estimated_value_saved_inr", "sum"),
            total_items_reused=("items_reused", "sum"),
            avg_reuse_factor=("estimated_material_reuse_factor", "mean"),
        ).reset_index()


# Convenience instances - will be initialized with correct paths
item_listings_manager: Optional[ItemListingManager] = None
sharing_activities_manager: Optional[SharingActivityManager] = None
user_manager: Optional[UserManager] = None
impact_manager: Optional[ImpactManager] = None


def init_managers(base_dir: str = ".") -> None:
    """Initialize managers with proper file paths."""
    global item_listings_manager, sharing_activities_manager, user_manager, impact_manager
    item_listings_manager = ItemListingManager(os.path.join(base_dir, "data", "item_listings.csv"))
    sharing_activities_manager = SharingActivityManager(os.path.join(base_dir, "data", "sharing_activities.csv"))
    user_manager = UserManager(os.path.join(base_dir, "data", "users.csv"))
    impact_manager = ImpactManager(os.path.join(base_dir, "data", "impact.csv"))