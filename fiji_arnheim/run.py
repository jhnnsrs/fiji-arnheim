from fiji_arnheim.helper import ImageJHelper
from grunnlag.schema import Representation
from bergen.clients.provider import ProviderBergen
from bergen.models import Node
from bergen.console import console
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--config', help='Which config file to use', default="bergen.yaml", type=str)
args = parser.parse_args()



def main():
    print(args)

    bergen_params = {
        "config_path": args.config
    }

    client = ProviderBergen(**bergen_params)
    client.negotiate()

    helper = ImageJHelper()

    show = Node.objects.get(package="Elements", interface="show")
    blur = Node.objects.get(package="Elements", interface="gaussian_blur")

    @client.template(show, gpu=True, image_k=True)
    async def show(rep: Representation) -> Representation:
        helper.displayRep(rep)
        return rep

    @client.template(blur, gpu=True, image_k=True)
    def blur(rep: Representation, int=3) -> Representation:
        rep = Representation.objects.get(id=rep.id)
        helper.displayRep(rep)
        return rep

    client.provide()


if __name__ == "__main__":
    main()








