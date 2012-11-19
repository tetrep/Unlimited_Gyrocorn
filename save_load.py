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
    #  @param data the object we want to load to
    #  @param filename the name of the file we are loading from
    def load_object(self, data, filename):
        #read file for reading
        file_in = open(filename, 'rb')

        #write to object from file
        data = pickle.load(file_in)

        #we're done with the file
        file_in.close()

    ## the save level function
    #  @brief saves the level and the round
    #  @param filename the name of the file we are saving to
    #  @param game the instance of the game we are saving from
    def save_level(self, filename, game):
        #ready file for writing
        file_out = open(filename, 'w')

        #write the data
        file_out.write(game.level + "\n" + game.selectedLevel)

        #close file
        file_out.close()

    ## the load level function
    #  @brief loads the level and the round
    #  @brief game the instance of the game we are loading to
    #  @brief filename the name of the file we are loading from
    def load_level(self, game, filename):
        #read file for reading
        file_in = open(filename, 'r')

        #read in level
        game.level = file_in.readline()
        game.selectedLevel = file_in.readline()

        #close file
        file_in.close()

    ## the save game function
    #  @brief saves the game
    #  @param game the game to save from
    #  @param filename the name of the save files, optional
    def save_game(self, game, filename = "test"):
        #save the players
        save_object(filename+"-players.save", game.players)

        #save the towers
        save_object(filename+"-towers.save", game.turrets)

        #save the maps
        save_object(filename+"-maps.save", game.maps)

        #save the round and level name
        save_level(filename+"-level.save", game)

    ## the load game function
    #  @brief loads the game
    #  @param game the game to load to
    #  @param filename the name of the save files, optional
    def load_game(self, game, filename = "test"):
        #load the players
        load_object(game.players, filename+"-players.save")

        #load the towers
        load_object(game.turrets, filename+"-towers.save")

        #load the maps
        load_object(game.maps, filename+"-maps.save")

        #load the round and level
        load_level(game, filename+"-level.save")
