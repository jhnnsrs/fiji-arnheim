#%%
from bergen.clients.provider import ProviderBergen
from bergen.models import Node
from bergen import use
import asyncio
import random
from aiostream import stream
import logging
from fiji_arnheim.helper import ImageJHelper
from fiji_arnheim.macros.filter import FilterMacro
from grunnlag.schema import Representation, RepresentationVariety, Sample
import xarray as xr


logger = logging.getLogger(__name__)


helper = ImageJHelper()



async def main():

    async with ProviderBergen() as client:

        blur = use(package="Elements", interface="gaussian_blur")
        show = use(package="Elements", interface="show")

        fft = FilterMacro("""
            stack = getImageID;
            run("FFT", stack);
            """)


        @client.template(blur, gpu=True, image_k=True)
        async def bluring(rep: Representation, sigma=None):
            """Sleep on the CPU

            Args:
                helper ([type]): [description]
                rep ([type], optional): [description]. Defaults to None.
            """
            array = fft(rep.data.sel(c=0, t=0, z=0))

            new = array.data.reshape(array.shape + (1,1,1))
            output = xr.DataArray(new, dims=list("xyczt"))
            rep = await Representation.asyncs.from_xarray(output, name="fft", sample= rep.sample.id, variety=RepresentationVariety.VOXEL)
            return rep

        @client.template(show, gpu=True, image_k=True)
        def show(rep: Representation):
            """Sleep on the CPU

            Args:
                helper ([type]): [description]
                rep ([type], optional): [description]. Defaults to None.
            """
            helper.displayRep(rep)
            return rep

        await client.provide_async()



    
if __name__ == "__main__":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()





