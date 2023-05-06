from cx_Freeze import setup, Executable

setup(name='creador_prompts',
      version='1.0',
      description='Genera contenido json para función creativa de OpenAI',
      executables=[Executable('creador_de_prompts.py')],
      options={
          'build_exe': {
              'packages': ['os', 'openai', 'requests', 'json'],
              'include_files': []
          }
      }
      )