#!/usr/bin/env python3

# =========================================================================
#
#   Copyright NumFOCUS
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#          https://www.apache.org/licenses/LICENSE-2.0.txt
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# =========================================================================


def test_create_study():
    """
    Purpose: Exercise the basic steps for creating a study dict, which is the precursor
    step to creating a dataset/dataloader for a machine learning framework such as
    TensorFlow or Torch.
    """
    import copy
    import histomics_stream as hs

    # Create a study and insert study-wide information
    my_study0 = {"version": "version-1"}
    my_study0["tile_height"] = 256
    my_study0["tile_width"] = 256
    my_slides = my_study0["slides"] = {}

    # Add a slide to the study, including slide-wide information with it.
    my_slide0 = my_slides["Slide_0"] = {}
    my_slide0[
        "filename"
    ] = "/tf/notebooks/histomics_stream/example/TCGA-BH-A0BZ-01Z-00-DX1.45EB3E93-A871-49C6-9EAE-90D98AE01913.svs"
    my_slide0["slide_name"] = "TCGA-BH-A0BZ-01Z-00-DX1"
    my_slide0["slide_group"] = "TCGA-BH-A0BZ"
    my_slide0["chunk_height"] = 2048
    my_slide0["chunk_width"] = 2048

    if False:
        # For each slide, find the appropriate resolution given the
        # desired_magnification and magnification_tolerance.  In this example, we use
        # the same parameters for each slide, but this is not required generally.
        find_slide_resolution = hs.configure.FindResolutionForSlide(
            my_study0, desired_magnification=20, magnification_tolerance=0.02
        )
        for slide in my_study0["slides"].values():
            find_slide_resolution(slide)
    else:
        # Because we don't actually have the image available, make up some numbers.
        my_slide0["level"] = 0
        my_slide0["factor"] = 0.5
        my_slide0["slide_width"] = 85047
        my_slide0["slide_height"] = 112334

    # We are going to demonstrate several approaches to choosing tiles.  Each approach
    # will start with its own copy of the my_study0 that we have built so far.

    # Demonstrate TilesByGridAndMask without a mask
    my_study_by_grid = copy.deepcopy(my_study0)
    tiles_by_grid = hs.configure.TilesByGridAndMask(
        my_study_by_grid, overlap_height=32, overlap_width=32, randomly_select=100
    )
    # We could apply this to a subset of the slides, but we will apply it to all slides
    # in this example.
    for slide in my_study_by_grid["slides"].values():
        tiles_by_grid(slide)

    if False:
        # Skip this test for now because we don't have the mask file available.
        # Demonstrate TilesByGridAndMask with a mask
        my_study_by_grid_and_mask = copy.deepcopy(my_study0)
        tiles_by_grid_and_mask = hs.configure.TilesByGridAndMask(
            my_study_by_grid_and_mask,
            overlap_height=0,
            overlap_width=0,
            mask_filename="/tf/notebooks/histomics_stream/example/TCGA-BH-A0BZ-01Z-00-DX1.45EB3E93-A871-49C6-9EAE-90D98AE01913-mask.png",
            randomly_select=100,
        )
        # We could apply this to a subset of the slides, but we will apply it to all
        # slides in this example.
        for slide in my_study_by_grid_and_mask["slides"].values():
            tiles_by_grid_and_mask(slide)

    # Demonstrate TilesByList
    my_study_by_list = copy.deepcopy(my_study0)
    tiles_by_list = hs.configure.TilesByList(
        my_study_by_list,
        randomly_select=5,
        tiles_dictionary=my_study_by_grid["slides"]["Slide_0"]["tiles"],
    )
    # We could apply this to a subset of the slides, but we will apply it to all slides
    # in this example.
    for slide in my_study_by_list["slides"].values():
        tiles_by_list(slide)

    # Demonstrate TilesRandomly
    my_study_randomly = copy.deepcopy(my_study0)
    tiles_randomly = hs.configure.TilesRandomly(my_study_randomly, randomly_select=3)
    # We could apply this to a subset of the slides, but we will apply it to all slides
    # in this example.
    for slide in my_study_randomly["slides"].values():
        tiles_randomly(slide)

    # The next step would be creating a dataset/dataloader for a machine learning
    # framework such as TensorFlow or Torch.  However, we will not do that in this test.


if __name__ == "__main__":
    test_create_study()
