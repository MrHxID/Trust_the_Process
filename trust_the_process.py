from itertools import permutations
from random import shuffle

__version__ = "2.1.2"


# Modify this for every event
participants: tuple[str, ...] = (
    "Pavlos",
    "Andres",
    "Konstantinos (aka bigman)",
    "Mara",
    # ? "Satyajit",
    "Stamatina",
    # ? "Teresa",
    "Leopold",
    # ? maybe some other people
)


# These may also change in the future
with open("README.md") as readme:
    rules = readme.read()

print(rules)


def random_perm(n: int) -> tuple[int, ...]:
    """Creates a random permutation ``p`` such that every element
    has been moved to a new position.

        Args:
            n (int): Number of participants.

        Returns:
            tuple[int, ...]: Permutation ``p``.
    """

    if n < 1:
        raise ValueError(
            f"Invalid number of participants. Expected n >= 1; got {n = }."
        )

    perms = list(permutations(range(n)))
    shuffle(perms)

    for p in perms:
        if not characteristic(p):
            break

    # Pylance will complain here that p might be unbound.
    # However, for n >= 1 there will always be at least one
    # permutation.
    return p  # type: ignore


def characteristic(p: list[int] | tuple[int, ...]) -> bool:
    """Checks if the permutation ``p`` contains the number ``i``
    at index ``i`` for all ``0 <= i < len(p)``.

    Args:
        p (list[int]): Permutation to check.

    Returns:
        bool: Whether the permutation contains an unswapped element.
    """

    for i in range(len(p)):
        if p[i] == i:
            return True

    return False


def main() -> None:
    n = len(participants)
    l = max(len(part) for part in participants)

    v = range(n)

    p = random_perm(n)

    order = tuple(f"{i}." for i in range(1, n + 1))
    senders = tuple(participants[i] for i in v)
    receivers = tuple(participants[p[i]] for i in v)

    table_header = ("Order", "Selector", "Presenter")
    process = zip(order, senders, receivers)

    # Widths for formatting
    w_order = len(table_header[0])
    w_selector = max(l, len(table_header[1]))
    w_presenter = max(l, len(table_header[2]))

    print(
        f"{table_header[0]} {table_header[1]:>{w_selector}}    {table_header[2]:>{w_presenter}}"
    )
    print("=" * (w_order + w_selector + w_presenter + 5))

    for p in process:
        # Some safety features to prevent non-sensical assignments. If the program crashes
        # here, this is a bug and should be reported to Leopold.
        assert p[1] != p[2]
        assert set(senders) == set(participants)
        assert set(receivers) == set(participants)
        print(
            f"{p[0]:>{len(table_header[0])}} {p[1]:>{max(l, len(table_header[1]))}} -> {p[2]:>{max(l, len(table_header[2]))}}"
        )


if __name__ == "__main__":
    main()
