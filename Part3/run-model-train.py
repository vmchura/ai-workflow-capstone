from model import model_train, model_load
import os
def main():
    print("Run model train")
    DATA_DIR = os.path.join('.', 'cs-train')
    ## train the model
    model_train(DATA_DIR, test=False)

    ## load the model
    model = model_load()
    
    print("model training complete.")


if __name__ == "__main__":

    main()
