import pickle
import copy
from pytruss import Mesh

DEFAULT_OPTIMIZATION_SETTINGS = {
    # optimization settings
    "member_cost": 10,
    "joint_cost": 10,
    "lr": 0.01,
    "epochs": 5000,
    "optimizer": "SGD",
    "min_member_length": 10,
    "max_member_length": 1000,
    "max_tensile_force": 10,
    "max_compressive_force": 10,
    "constraint_aggression": 2,
    "progress_bar": True,
    "show_metrics": False,
    "update_metrics_interval": 100,
    "save_frequency": 1000,
    "save_path": None,
    "frame_rate": 1,
}

DEFAULT_VIEW_PREFERENCES = {
    "support_color": (255, 100, 100),
    "support_size": 10,
    "member_color": (0, 0, 0),
    "member_size": 1,
    "force_color": (0, 0, 0),
    "force_head_width": 3,
    "force_head_length": 6,
    "scale_factor": 10,
    "joint_color": (100, 100, 255),
    "joint_focused_color": (50, 50, 255),
    "joint_radius": 5,
}


class SavedTruss:
    """Handles creating of truss save object that will be pickled. This object should be made before every save event to ensure all new features and settings are acounted for."""

    def __init__(self, truss: Mesh, optimization_settings: dict = copy.copy(DEFAULT_OPTIMIZATION_SETTINGS), view_preferences: dict = copy.copy(DEFAULT_VIEW_PREFERENCES)) -> None:
        self.truss = truss
        self.optimization_settings = optimization_settings
        self.view_preferences = view_preferences

    def save(self, file: str, optional_suffix="", optional_prefix="") -> None:
        """Saves the truss and settings."""
        with open(optional_prefix + file + optional_suffix + ("" if file.endswith(".trss") else ".trss"), "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(file: str, safe_load=False) -> "SavedTruss":
        """Loads the truss and settings."""
        with open(file, "rb") as f:
            saved_truss: Mesh | SavedTruss = pickle.load(f)

        if isinstance(saved_truss, Mesh):
            loaded_truss = SavedTruss(saved_truss)
        elif safe_load:
            loaded_truss = SavedTruss(saved_truss.truss)
        # incase savedtruss object is old and doesnt have newer features
        else:
            loaded_truss = SavedTruss(saved_truss.truss)
            if hasattr(saved_truss, "optimization_settings"):
                # loop thru incase new settings since the truss was saved
                for key, val in saved_truss.optimization_settings.items():
                    loaded_truss.optimization_settings[key] = val
            if hasattr(saved_truss, "view_preferences"):
                # loop thru incase new settings since the truss was saved
                for key, val in saved_truss.view_preferences.items():
                    loaded_truss.view_preferences[key] = val

        return loaded_truss
