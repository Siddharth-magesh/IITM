import docker
import time
from pathlib import Path

client = docker.from_env()

script_dir = Path(__file__).resolve().parent
print(f'Building image ga2-25c816:latest from {script_dir!s}...')
image, build_logs = client.images.build(path=str(script_dir), tag='ga2-25c816:latest')
print('Built:', image.tags)

print('Running container (mapped 7167)...')
container = client.containers.run('ga2-25c816:latest', ports={'7167/tcp': 7167}, detach=True)
print('Container id:', container.id)
print('Give the app a few seconds to start...')
time.sleep(5)
print('Container logs:\n', container.logs(tail=50).decode('utf-8'))

print('To stop: container.stop(); container.remove()')
