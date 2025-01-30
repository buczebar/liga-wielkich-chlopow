#!/usr/bin/python3

import argparse
import json
import os


def extract_profile_from_workout(workout_file):
    with open(workout_file, "r") as f:
        workout = json.load(f)

    profile = []

    for segment in workout.get("workoutSegments", []):
        for step in segment.get("workoutSteps", []):
            if step.get("type") == "RepeatGroupDTO":
                for inner_step in step.get("workoutSteps", []):
                    if inner_step.get("exerciseName"):
                        profile.append(
                            {
                                "exerciseName": inner_step.get("exerciseName"),
                                "weightValue": inner_step.get("weightValue"),
                                "reps": inner_step.get("endConditionValue"),
                            }
                        )
            elif step.get("exerciseName"):
                profile.append(
                    {
                        "exerciseName": step.get("exerciseName"),
                        "weightValue": step.get("weightValue"),
                        "reps": step.get("endConditionValue"),
                    }
                )

    return profile


def combine_profiles(template_files):
    combined_profiles = []

    for workout_file in template_files:
        if os.path.exists(workout_file):
            config = extract_profile_from_workout(workout_file)
            for item in config:
                if item not in combined_profiles:
                    combined_profiles.append(item)
        else:
            print(f"Warning: Workout file '{workout_file}' does not exist.")

    return combined_profiles


def main():
    parser = argparse.ArgumentParser(
        description="Create profile JSON from multiple workout files."
    )
    parser.add_argument(
        "-w", "--workouts", required=True, nargs="+", help="Paths to workout files"
    )
    parser.add_argument(
        "-o", "--output", required=True, help="Path to the output profile file"
    )
    args = parser.parse_args()

    try:
        config = combine_profiles(args.workouts)

        with open(args.output, "w") as f:
            json.dump(config, f, indent=5)

        print(f"Profile file created successfully at {args.output}")
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()
