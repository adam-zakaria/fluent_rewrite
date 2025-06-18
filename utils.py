import os

def basename(file_path):
  # i.e. /a/b/c/d.mp4 -> d.mp4
  return os.path.basename(file_path)

def key(file_path):
  """
  Example:
    /a/b/c/d.mp4
    -> d
  """
  # Split the path by '/'
  path_parts = file_path.split('/')

  # Extract the last part (filename) and then split by '.' to remove the extension
  file_name_without_extension = path_parts[-1].split('.')[0]

  return file_name_without_extension

def ls(dir):
  """
  Returns [dir/child_dir1, dir/child_dir2, ...]

  Example:
  utils.ls('twitch_streams')
  -> ['twitch_streams/royal2','twitch_streams/renegade',...]
  """
  return [os.path.join(dir, f) for f in os.listdir(dir)]
