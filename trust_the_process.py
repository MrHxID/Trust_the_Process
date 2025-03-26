import random
from itertools import permutations

__version__ = "2.0.0"


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
rules = """ACHTUNG!!!
Please note that the rules have not yet been peer-reviewed and may change in the future.

These are the rules of the "Process Presentation Game" (name is subject to change):

1.  The participants have to agree on a preparation time, e.g. 1h. The time span
    has to be decided before the topics are selected.
2.  Each participant chooses a topic that another participant has to prepare
    a presentation for. The assignment of who selects a topic for whom is made
    by this program (see table "Selector -> Presenter").
3.  The slides should look as unprofessional as possible. The more brain cells are
    lost per slide, the better. Any means of creating eyesores is allowed
    and even encouraged.
4.  After the preparation time is over, the participants present their talks in the
    order given by this programm. The talk should generally be held in a way as if
    you were presenting a serious topic. The goal is to create dry humour and spontaneous
    jokes that the audience does not expect.
5.  Any participant who is unwilling to present the topic assigned to them will have their
    bigman-certificate taken away from them until they can deliver a satisfactory talk.
"""

print(rules)

n = len(participants)
l = max(len(part) for part in participants)


def main():

    M = create_shuffled_matrix()

    v = list(range(n))

    order = tuple(f"{i}." for i in range(1, n + 1))
    senders = tuple(participants[i] for i in v)
    receivers = tuple(participants[matmul(M, v)[i]] for i in v)

    table_header = ("Order", "Selector", "Presenter")
    process = zip(order, senders, receivers)

    print(
        f"{table_header[0]} {table_header[1]:>{max(l, len(table_header[1]))}}    {table_header[2]:>{max(l, len(table_header[2]))}}"
    )
    print(
        "="
        * (
            len(table_header[0])
            + max(l, len(table_header[1]))
            + max(l, len(table_header[2]))
            + 5
        )
    )

    for p in process:
        # Some safety features to prevent non-sensical assignments. If the program crashes
        # here, this is a bug and should be reported to Leopold.
        assert p[1] != p[2]
        assert set(senders) == set(participants)
        assert set(receivers) == set(participants)
        print(
            f"{p[0]:>{len(table_header[0])}} {p[1]:>{max(l, len(table_header[1]))}} -> {p[2]:>{max(l, len(table_header[2]))}}"
        )


def matmul(M: list[list[int]], v: list[int]) -> list[int]:
    """Perform an integer matrix-vector multiplication.

    Args:
        M (list[list[int]]): Matrix.
        v (list[int]): Vector.

    Returns:
        list[int]: Output vector.
    """

    n = len(v)
    out: list[int] = []

    for row in M:
        assert len(row) == n, "Shape of matrix and vector don't match."
        out.append(sum(row[i] * v[i] for i in range(n)))

    return out


def create_shuffled_matrix() -> list[list[int]]:
    """Creates a matrix, that has exactly one ``1`` in each
    row and column and ``0`` otherwise.

    Returns:
        list[list[int]]: Matrix.
    """

    perms = list(permutations(range(n)))

    while True:
        p = random.choice(perms)

        # Only select permutations that change the location of every
        # element to prevent people from assigning topics to themselves.
        if not characteristic(p):
            break

    M: list[list[int]] = []

    for i in range(n):
        row = [0] * n
        row[p[i]] = 1
        M.append(row)

    return M


def characteristic(p: list[int] | tuple[int, ...]) -> bool:
    """Checks if the permutation ``v`` contains the number ``i``
    at index ``i`` for all ``0 <= i < len(v)``.

    Args:
        p (list[int]): Permutation to check.

    Returns:
        bool: Whether the permutation contains an unswapped element.
    """

    for i in range(len(p)):
        if p[i] == i:
            return True

    return False


if __name__ == "__main__":
    main()
