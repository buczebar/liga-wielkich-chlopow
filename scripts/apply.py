#!/usr/bin/python3

import argparse
import json


def update_step(step, config):
    exercise_name = step.get("exerciseName")
    if not exercise_name:
        return

    for conf in config:
        if conf.get("exerciseName") == exercise_name:
            if "weightValue" in conf:
                step["weightValue"] = conf["weightValue"]
            if "reps" in conf:
                step["endConditionValue"] = conf["reps"]
            break


def update_json(config_file, template_file):
    with open(config_file, "r") as f:
        config = json.load(f)

    with open(template_file, "r") as f:
        template = json.load(f)

    for segment in template.get("workoutSegments", []):
        for step in segment.get("workoutSteps", []):
            if step.get("type") == "RepeatGroupDTO":
                for inner_step in step.get("workoutSteps", []):
                    update_step(inner_step, config)
            else:
                update_step(step, config)

    return template


def main():
    parser = argparse.ArgumentParser(
        description="Update JSON workout template based on profile file."
    )
    parser.add_argument(
        "-p", "--profile", required=True, help="Path to the profile file"
    )
    parser.add_argument(
        "-w", "--workout", required=True, help="Path to the workout file"
    )
    args = parser.parse_args()

    try:
        updated_json = update_json(args.profile, args.workout)
        print(json.dumps(updated_json, indent=5))
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()
