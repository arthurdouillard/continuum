from typing import Callable, List, Tuple

import numpy as np

from clloader.task_set import TaskSet
from clloader.datasets import _ContinuumDataset
from clloader.scenarios import TransformationIncremental

from torchvision import transforms


class Rotations(TransformationIncremental):
    """Continual Loader, generating datasets for the consecutive tasks.
    Scenario: Mode incremental scenario is a new instance scenario where we explore the distribution mode by mode.
              For example rotation mnist, is a exploration of the distribution by rotation angles, each angle can be
              seen as a mode of the distribution. Same for permutMnist, mode=permutations space.

    :param cl_dataset: A continual dataset.
    :param increment: Either number of classes per task, or a list specifying for
                      every task the amount of new classes.
    :param initial_increment: A different task size applied only for the first task.
                              Desactivated if `increment` is a list.
    :param train_transformations: A list of data augmentation applied to the train set.
    :param common_transformations: A list of transformations applied to both the
                                   the train set and the test set. i.e. normalization,
                                   resizing, etc.
    :param incremental_transformations: A list of transformations specific to each tasks. e.g. rotations, permutations
    """

    def __init__(
            self,
            cl_dataset: _ContinuumDataset,
            nb_tasks: int,
            list_degrees: List[Tuple],
            base_transformations: List[Callable] = None,
            train=True
    ):

        if len(list_degrees) != nb_tasks:
            raise ValueError("The number of tasks is not equal to the number of angles tuples set in the list")

        list_transformations = []
        min, max = 0, 0
        for tuple in list_degrees:
            if type(tuple) == int:
                min = tuple
                max = tuple
            elif len(tuple) == 2:
                min, max = tuple
            else:
                raise ("list_degrees should contains list of rotations either with only one angle or with (min,max)")

            list_transformations.append([transforms.RandomAffine(degrees=[min, max])])

        super().__init__(
            cl_dataset=cl_dataset,
            nb_tasks=nb_tasks,
            incremental_transformations=list_transformations,
            base_transformations=base_transformations,
            train=train
        )
