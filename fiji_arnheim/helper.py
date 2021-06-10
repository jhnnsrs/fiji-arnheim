from grunnlag.schema import Representation
from fiji_arnheim.registries.helper import BaseImageJHelper, set_running_helper
import dask

class ImageJHelper(BaseImageJHelper):

    def __init__(self, headless=False, bind=True, version="sc.fiji:fiji:2.1.1", plugins = []) -> None:
        if bind: set_running_helper(self)
        super().__init__(headless=headless, version=version, plugins= plugins)


    def displayRep(self, rep: Representation):
        image = rep.data

        if "z" in image.dims:
            image = image.max(dim="z")
        if "t" in image.dims:
            image = image.sel(t=0)
        if "c" in image.dims:
            image = image.sel(c=0)

        if dask.is_dask_collection(image.data):
            jimage = self.py.to_java(image.compute())
        else:
            jimage = self.py.to_java(image)

        # Convert the Image to Image
        self.ui.show(rep.name, jimage)