def find_duplicate_blocks(source):
    raw_lines = source.splitlines()

    code_lines = []

    for line_number, line in enumerate(raw_lines, start=1):
        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith("#"):
            continue

        code_lines.append((line_number, stripped))

    block_size = 3
    blocks = {}

    for i in range(len(code_lines) - block_size + 1):
        block = tuple(
            code_lines[j][1]
            for j in range(i, i + block_size)
        )

        start_line = code_lines[i][0]

        blocks.setdefault(block, []).append(start_line)

    candidates = []

    for block, locations in blocks.items():
        if len(locations) >= 2:
            candidates.append(
                {
                    "lines": list(block),
                    "locations": locations,
                }
            )

    # Process blocks with more occurrences first.
    candidates.sort(
        key=lambda item: len(item["locations"]),
        reverse=True,
    )

    duplicates = []

    for candidate in candidates:
        candidate_lines = candidate["lines"]
        candidate_locations = candidate["locations"]

        is_artificial_overlap = False

        for accepted in duplicates:
            accepted_lines = accepted["lines"]
            accepted_locations = accepted["locations"]

            # Only suppress a candidate when a stronger duplicate
            # has more occurrences.
            if len(candidate_locations) >= len(accepted_locations):
                continue

            block_length = len(accepted_lines)

            for shift in range(1, block_length):
                rotated = (
                    accepted_lines[shift:]
                    + accepted_lines[:shift]
                )

                expected_locations = [
                    location + shift
                    for location in accepted_locations[
                        :len(candidate_locations)
                    ]
                ]

                if (
                    candidate_lines == rotated
                    and candidate_locations == expected_locations
                ):
                    is_artificial_overlap = True
                    break

            if is_artificial_overlap:
                break

        if not is_artificial_overlap:
            duplicates.append(candidate)

    return duplicates