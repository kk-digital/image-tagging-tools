from PIL import Image
import os 
import torch


def clip_image_features(image_path , model , preprocess , device):
    """ returns the features of the image using OpenClip"""    
    with torch.no_grad():
        image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
        return model.encode_image(image).detach().numpy()

def classify_image(image_path , classifier , mapper, 
                  clip_model , preprocess , device):
    """Returns the string of "tag" or "other" """
    image_features = clip_image_features(image_path , clip_model , preprocess , device)
    return mapper[str(classifier.predict(image_features)[0])]

def convert_gif_to_image(gif_path):
    """ Delets the GIF and change it with first frame .png image  """
    im  = Image.open(gif_path)
    dir_path = os.path.dirname(os.path.abspath(gif_path))
    im.seek(0)
    im_file = os.path.basename(gif_path).split('.gif')[0]
    save_path = os.path.join(dir_path ,f'{im_file}.png' )
    im.save(save_path) # save the first frame as .png image 
    os.system(f'rm -r {gif_path}') # Delete the .gif file 

def clean_file(file_path):
  """ This function takes a file path and see if it is supported or not 
    :file_path: path of the file to work with 
  """
  if file_path.lower().endswith('.gif'): # If it's GIF then convert to image and exit 
    try : 
      convert_gif_to_image(file_path)
    except:
      print(f"[Warning] problem with {file_path}")
      if os.path.exists(file_path):
        print(f"[Warning] removing {file_path}")
        os.system(f'rm {file_path}')
    return 

  # if it's not gif and not a supprted file type then remove it 
  if not file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif', '.tiff', '.webp')):
    os.system(f'rm {file_path}')
    print(f'[Removing] {file_path}')
    return 

def clean_directory(dir_path , only_sub_dir = False):
  """ Clean a directory 
      -- check if it has directory or image 
      -- take action based on this 
     :dir_path: path of the directory to be cleaned 
     :only_sub_dir: key for having only sub dirs not sub files 
                    for example in 'pixel-art-tagged'
  """
  for dir in os.listdir(dir_path):
    sub_dir = os.path.join(dir_path, dir)
    
    if os.path.isfile(sub_dir): # if it's a file then clean the file  
      
      if only_sub_dir : # no subfiles allowed for example in the pixel-art-tagged 
        os.system(f'rm  {sub_dir}') 
        print(f"[Removing] {sub_dir}")
        continue 
      clean_file(sub_dir)
      continue

    if len(os.listdir(sub_dir)) == 0: # Empty folder, delte it 
      os.system(f'rm -r {sub_dir}') 
      print(f'[Removing] {sub_dir}')
      continue

    if os.path.isdir(sub_dir):
      clean_directory(sub_dir)