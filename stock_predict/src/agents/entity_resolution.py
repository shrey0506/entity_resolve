from rapidfuzz import fuzz, process
from pandas import DataFrame, Series
from typing import Optional, Tuple

class EntityResolutionAgent:
    def __init__(self, dnb_df: DataFrame, cmd_df: DataFrame):
        """
        Initialize the EntityResolutionAgent with D&B and CMD dataframes.

        Args:
            dnb_df (pd.DataFrame): DataFrame containing D&B entity data.
            cmd_df (pd.DataFrame): DataFrame containing CMD entity data.
        """
        self.dnb = dnb_df
        self.cmd = cmd_df

    def resolve(self, name: str, postal: str) -> Tuple[Optional[Series], Optional[Series]]:
        """
        Resolve an entity by name and postal code using D&B and CMD datasets.

        Args:
            name (str): The entity name to resolve.
            postal (str): The postal code to filter candidates.

        Returns:
            Tuple[Optional[pd.Series], Optional[pd.Series]]:
                - The best-matched D&B entity row (or None if not found).
                - The best-matched CMD entity row (or None if not found).
        """
        # Step 1: lookup in D&B
        candidates = self.dnb[self.dnb["postal_code"] == postal]
        if candidates.empty:
            return None, None
        dnb_entity = process.extractOne(name, candidates["name"], scorer=fuzz.WRatio)
        dnb_row = candidates[candidates["name"] == dnb_entity[0]].iloc[0]

        # Step 2: lookup in CMD
        cmd_candidates = self.cmd[self.cmd["postal_code"] == postal]
        if cmd_candidates.empty:
            return dnb_row, None
        cmd_entity = process.extractOne(name, cmd_candidates["name"], scorer=fuzz.WRatio)
        cmd_row = cmd_candidates[cmd_candidates["name"] == cmd_entity[0]].iloc[0]

        return dnb_row, cmd_row
