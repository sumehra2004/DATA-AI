from fabric import Connection

def deploy():
    c = Connection("localhost")

    c.run("echo Deploying application")
    c.put("deploy.zip", "/tmp/deploy.zip")

    print("Deployment complete")

if __name__ == "__main__":
    deploy()
