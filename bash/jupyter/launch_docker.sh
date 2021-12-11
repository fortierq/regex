firefox $(docker logs mp2i_devcontainer_jupyter_1 2>&1 | grep -Eo "http://127.0.0.1[^ ]*" | head -n 1)
