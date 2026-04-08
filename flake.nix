{
  description = "Dockerized Dev Environment for React and Python";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };

      # Your custom Python setup
      myPython = pkgs.python3.withPackages (ps: with ps; [
        fastapi
        uvicorn
        pandas
        requests
        fastapi
        numpy
        pandas
      ]);

      # The environment contents
      devEnv = with pkgs; [
        bashInteractive
        coreutils
        nodejs_20
        nodePackages.tailwindcss
        myPython
        git
        curl
      ];
      devImage = pkgs.dockerTools.buildImage {
        name = "dev-machine";
        tag = "latest";

        # This creates the standard Linux directory structure inside the container
        copyToRoot = pkgs.buildEnv {
          name = "image-root";
          paths = devEnv;
          pathsToLink = [ "/bin" ];
        };

        config = {
          Cmd = [ "/bin/bash" ];
          WorkingDir = "/data";
          # Open ports for Vite and FastAPI
          ExposedPorts = {
            "5173/tcp" = { };
            "8000/tcp" = { };
          };
        };
      };

      runScript = pkgs.writeShellScriptBin "run-dev-container" ''
        set -e
              # Use a specific tag to avoid 'latest' caching issues
              IMAGE_NAME="tailwind-dev-machine"
              TAG="nix-build"

              echo "🔨 Loading Nix-built image into Docker..."
              # We use --quiet to keep the logs clean, then pipe the image in
              docker load < ${devImage}

              echo "🔍 Verifying image availability..."
              if ! docker image inspect "$IMAGE_NAME:$TAG" >/dev/null 2>&1; then
                # Fallback: find the image ID if the tag didn't apply correctly
                IMAGE_ID=$(docker load < ${devImage} | grep "Loaded image" | awk '{print $3}')
                docker tag "$IMAGE_ID" "$IMAGE_NAME:$TAG"
              fi

              echo "🚀 Starting Frontend Dev Server..."
              # Force the use of the specific tag we just verified
              docker run -it --rm \
                -v "$(pwd):/data" \
                --workdir "/data/frontend" \
                -p 5173:5173 \
                -p 8000:8000 \
                "$IMAGE_NAME:$TAG" \
                /bin/bash -c "npm install --force && (npm run dev -- --host || echo '❌ Dev server failed. Staying in shell for debugging...'); exec /bin/bash"
      '';
      devShell = pkgs.mkShell {
        buildInputs = devEnv;
        shellHook = "source .venv/bin/activate";
      };
    in
    {
      devShells.${system}.default = devShell;
      packages.${system}.default = devImage;
      apps.${system}.default = {
        type = "app";
        program = "${runScript}/bin/run-dev-container";
      };

    };
}
