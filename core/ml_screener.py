from sklearn.ensemble import RandomForestRegressor

from physics import (
    estimate_flight_time
)


def build_training_data(designs):

    X = []
    y = []

    for d in designs:

        X.append([
            d.get("wing_area_m2", 0),
            d.get("drag_coefficient", 0),
            d.get("estimated_weight_kg", 0),
            d.get("battery_mAh", 0),
            d.get("propeller_diameter_inch", 0)
        ])

        y.append(
            estimate_flight_time(d)
        )

    return X, y


def train_screener(designs):

    X, y = build_training_data(
        designs
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(
        X,
        y
    )

    return model


def predict_flight_time(
        model,
        design
):

    X = [[
        design.get(
            "wing_area_m2",
            0
        ),
        design.get(
            "drag_coefficient",
            0
        ),
        design.get(
            "estimated_weight_kg",
            0
        ),
        design.get(
            "battery_mAh",
            0
        ),
        design.get(
            "propeller_diameter_inch",
            0
        )
    ]]

    return model.predict(X)[0]