import rasterio
from rasterio.merge import merge
from glob import glob
import os
import matplotlib.pyplot as plt
import numpy as np

def run_mosaic(folder_path):
    tif_files = sorted(glob(os.path.join(folder_path, "*.TIF")))
    datasets = [rasterio.open(fp) for fp in tif_files]

    mosaic, out_trans = merge(datasets)
    out_meta = datasets[0].meta.copy()
    out_meta.update({
        "driver": "GTiff",
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": out_trans
    })

    output_tif = "static/output.tif"
    with rasterio.open(output_tif, "w", **out_meta) as dest:
        dest.write(mosaic)

    # ✅ Save preview image
    if mosaic.shape[0] >= 3:
        rgb = np.stack([mosaic[0], mosaic[1], mosaic[2]], axis=-1).astype(np.float32)
        rgb /= 255.0 if rgb.max() > 1 else 1.0
        plt.imshow(rgb)
    else:
        plt.imshow(mosaic[0], cmap='gray')

    plt.axis('off')
    plt.savefig("static/output.png", bbox_inches='tight')
    plt.close()

    return output_tif  # Optional: return output path
