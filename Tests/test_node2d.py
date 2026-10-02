import numpy as np

from Scene.Node2d import Node2d


def test_world_transform_with_90_degree_rotation():

    node = Node2d(
        position=[10, 20],
        theta=90
    )

    result = node.get_world_transform()

    expected = np.array([
        [0, -1, 10],
        [1,  0, 20],
        [0,  0,  1]
    ])

    np.testing.assert_allclose(
        result,
        expected,
        atol=1e-10
    )
    
def test_child_world_transform_without_rotation():

    parent = Node2d(
        position=[10, 20],
        theta=0
    )

    child = Node2d(
        position=[5, 3],
        theta=0
    )

    parent.add_child(child)

    result = child.get_world_transform()

    expected = np.array([
        [1, 0, 15],
        [0, 1, 23],
        [0, 0, 1]
    ])

    np.testing.assert_allclose(result, expected)
    
def test_child_world_transform_with_rotation():

    parent = Node2d(
        position=[10, 20],
        theta=90
    )

    child = Node2d(
        position=[1, 1],
        theta=0
    )

    parent.add_child(child)

    expected = np.array([
        [0, -1, 9],
        [1,  0, 21],
        [0,  0, 1]
    ])

    result = child.get_world_transform()

    np.testing.assert_allclose(
        result,
        expected,
        atol=1e-10
    )
    
def test_three_level_world_transform():

    grandparent = Node2d(
        position=[10, 0],
        theta=90
    )

    parent = Node2d(
        position=[2, 0],
        theta=0
    )

    child = Node2d(
        position=[3, 0],
        theta=0
    )

    grandparent.add_child(parent)
    parent.add_child(child)

    result = child.get_world_transform()

    expected = np.array([
        [0, -1, 10],
        [1,  0, 5],
        [0,  0, 1]
    ])

    np.testing.assert_allclose(
        result,
        expected,
        atol=1e-10
    )