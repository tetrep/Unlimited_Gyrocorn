import pickle

##   @class SaveLoad
#    @brief this class handles saving and loading the game
class SaveLoad(object):
    ## the constructor
    #  @param game the instance of the game that we will be saving/loading
    def __init(self):
        pass

    ## the save object function
    #  @brief pickles the given object and saves it to the given filename
    #  @param filename the name of the file we are saving to
    #  @param data the object we want to save
    def save_object(self, filename, data):
        #ready file for writing
        file_out = open(filename, 'wb')

        #save object using highest pickle protocol available
        pickle.dump(data, file_out, -1)

        #we're done with the file
        file_out.close()

    ## the load object function
    #  @brief unpickles the given file and stores it in the given object
    #  @param filename the name of the file we are loading from
    #  @param data the object we want to load to
    def load_object(self, data, filename):
        #read file for reading
        file_in = open(filename, 'rb')

        #write to object from file
        data = pickle.load(file_in)

        #we're done with the file
        file_in.close()
