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
        try:
           #save the players
            for player in game.players:
                player.game = None
                self.save_object(filename+"-players.save", game.players)
            for player in game.players:
                    player.game = game

            #save the towers
            self.save_object(filename+"-towers.save", game.turrets)

            #save the maps
            self.save_object(filename+"-tiles.save", game.tiles)

            #save the round and level name
            self.save_level(filename+"-level.save", game)
        except Exception as e:
            print e

####DO NOT CALL THIS FUNCTION####
####it returns None just to be safe####
    ## the load game function
    #  @brief loads the game
    #  @param game the game to load to
    #  @param filename the name of the save files, optional
    def load_game(self, game, filename = "test"):
        return None
        #load the players
        self.load_object(game.players, filename+"-players.save")

        #load the towers
        self.load_object(game.turrets, filename+"-towers.save")

        #load the maps
        self.load_object(game.tiles, filename+"-tiles.save")

        #load the round and level
        self.load_level(game, filename+"-level.save")
