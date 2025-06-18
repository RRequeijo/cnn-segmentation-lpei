import os
from PIL import Image
import numpy as np
from concurrent.futures import ProcessPoolExecutor

def is_black_image(image_path, threshold=10):
    try:
        img = Image.open(image_path).convert('RGB')
        np_img = np.array(img)
        return np.all(np_img < threshold)
    except Exception as e:
        print(f"Erro ao processar {image_path}: {e}")
        return False

def process_image(file_path):
    if is_black_image(file_path):
        return file_path
    return None

def remove_black_images_parallel(folder_path, max_workers=8):
    images = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))
    ]

    print(f"Encontradas {len(images)} imagens para analisar.")

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_image, images))

    black_images = [img for img in results if img is not None]

    print(f"Encontradas {len(black_images)} imagens pretas. Removendo...")

    log_path = os.path.join(folder_path, "removidas.log.txt")
    with open(log_path, 'w') as log_file:
        for img_path in black_images:
            try:
                os.remove(img_path)
                log_file.write(f"{os.path.basename(img_path)}\n")
                print(f"Removido: {img_path}")
            except Exception as e:
                print(f"Erro ao remover {img_path}: {e}")

    print(f"Processo concluído! Log salvo em: {log_path}")

if __name__ == "__main__":
    pasta = r"C:\Users\mfreq\Desktop\UTAD\Semestre 2\LPEI\fase2\PipelineVscode\vale-da-vilarica-corrigir-dataset-original"
    remove_black_images_parallel(pasta)