import pandas as pd
from pandas import DataFrame, Series
from typing import Optional

class TraversalAgent:
    """
    Agent for traversing hierarchical entity relationships in a CMD DataFrame.
    """

    def __init__(self, cmd_df: DataFrame):
        """
        Initialize the TraversalAgent with a CMD DataFrame.

        Args:
            cmd_df (pd.DataFrame): DataFrame containing CMD entity data.
        """
        self.cmd = cmd_df

    def get_parent(self, entity_id: int) -> Optional[DataFrame]:
        """
        Get the parent entity row for a given entity ID.

        Args:
            entity_id (int): The entity ID whose parent is to be found.

        Returns:
            Optional[pd.DataFrame]: DataFrame row of the parent entity, or None if not found.
        """
        row = self.cmd[self.cmd["entity_id"] == entity_id]
        if row.empty:
            return None
        parent_id = row.iloc[0]["parent_id"]
        if pd.isna(parent_id):
            return None
        return self.cmd[self.cmd["entity_id"] == parent_id]

    def get_children(self, entity_id: int) -> DataFrame:
        """
        Get all child entities for a given entity ID.

        Args:
            entity_id (int): The entity ID whose children are to be found.

        Returns:
            pd.DataFrame: DataFrame of child entities.
        """
        return self.cmd[self.cmd["parent_id"] == entity_id]

    def get_siblings(self, entity_id: int) -> DataFrame:
        """
        Get all sibling entities for a given entity ID.

        Args:
            entity_id (int): The entity ID whose siblings are to be found.

        Returns:
            pd.DataFrame: DataFrame of sibling entities.
        """
        row = self.cmd[self.cmd["entity_id"] == entity_id]
        if row.empty:
            return self.cmd.iloc[0:0]  # Return empty DataFrame
        parent_id = row.iloc[0]["parent_id"]
        return self.cmd[
            (self.cmd["parent_id"] == parent_id) & (self.cmd["entity_id"] != entity_id)
        ]
