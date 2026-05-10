from dataclasses import dataclass


@dataclass
class Asset:
    asset_name: str
    asset_type: str
    current_value: float
    monthly_contribution: float
