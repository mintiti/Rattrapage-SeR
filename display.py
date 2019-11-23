import pygame

# CONSTANTS :
WHITE = (255,255,255)
BLACK = (0,0,0)
R = (255,0,0)
G = (0,255,0)
B = (0,0,255)

STEINER_SIZE = (32,32)
DISPLAY_SIZE = (1920,1080)
GRID_UPSCALE_FACTOR = 100
#Rescaling constant

successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))

screen = pygame.display.set_mode(DISPLAY_SIZE)
pygame.display.set_caption('Rattrapage SeR')
clock = pygame.time.Clock()
FPS = 60  # Frames per second.

#Helper Functions
def upscale(coordinates):
    (x,y) = coordinates
    return (x * GRID_UPSCALE_FACTOR, y * GRID_UPSCALE_FACTOR)
#Graph object surfaces
class Clients :
    def __init__(self,position):
        self.image = pygame.Surface(STEINER_SIZE, pygame.SRCALPHA)
        self.rect = pygame.draw.polygon(self.image,WHITE,[(0,STEINER_SIZE[0]), (STEINER_SIZE[0], STEINER_SIZE[0]), (STEINER_SIZE[0] //2,0)])
        self.rect.center = position



class Steiner :
    def __init__(self,position):
        self.image = pygame.Surface(STEINER_SIZE)
        self.image.fill(WHITE)
        self.rect = pygame.Rect(position,STEINER_SIZE)
        self.rect.center = position

class EndOffices :
    def __init__(self,position):
        radius = round(STEINER_SIZE[0] / 2)
        self.position = position
        self.image = pygame.Surface(STEINER_SIZE, pygame.SRCALPHA)
        self.rect = pygame.draw.circle(self.image,WHITE,(radius,radius),radius)
        self.rect.center = self.position

    def draw(self,screen):
        screen.blit(self.image, self.rect)


    def move_up(self):
        self.position = (self.position[0],self.position[1]-1)

    def move_down(self):
        self.position = (self.position[0],self.position[1] + 1)

    def move_right(self):
        self.position = (self.position[0] + 1,self.position[1])

    def move_left(self):
        self.position = (self.position[0] -1,self.position[0])

class Background :
    def __init__(self, env):
        """
        à appeler pour recuperer l'image du background
        :param env: l'environnement pour lequel on desisne l'image
        """
        self.reseau_telecom = env.reseau_telecom
        (x,y) = self.reseau_telecom.grid_size
        self.image = pygame.Surface((x*100, y*100))
        self.image.fill(BLACK)
        bounding_box = self.image.get_bounding_rect()
        pygame.draw.rect(self.image , R, bounding_box, 1)

        #draw the steiner nodes
        self.list_steiners = []

        for steiner in self.reseau_telecom.steiners :
            self.list_steiners.append(Steiner(upscale(steiner)))

        for s in self.list_steiners :
            self.image.blit(s.image,s.rect)

        #draw the end offices
        self.list_end_offices = []

        for end in self.reseau_telecom.target_nodes :
            coordinate = (end[0] * 100 , end[1] * 100)
            self.list_end_offices.append(EndOffices(coordinate))
        for end in self.list_end_offices :
            end.draw(self.image)

        #draw the clients
        self.list_clients = []
        for client in self.reseau_telecom.clients :
            coordinate = (client[0] * 100, client[1] * 100)
            self.list_clients.append(Clients(coordinate))
        for client in self.list_clients :
            self.image.blit(client.image, client.rect)
class Lines :
    def __init__(self,agent,telecom):
        """

        :param agent: la solution pour laquelle on dessine
        :param telecom : juste l'environnement, sans la solution type ReseauTelecom
        """
        # Unpack solution
        C_target_steiner = agent.X
        C_client_target = agent.Z
        cycle_steiner = agent.Y
        print(cycle_steiner)

        # Unpack telecom
        (x,y) = telecom.grid_size
        steiners = telecom.steiners
        target_nodes = telecom.target_nodes
        clients = telecom.clients

        # Initialize the pygame.Surface
        self.image = pygame.Surface((x*GRID_UPSCALE_FACTOR, y* GRID_UPSCALE_FACTOR), pygame.SRCALPHA)
        #draw the lines between the steiner nodes
        for i in range(len(cycle_steiner) -1):
            pos1 = upscale(steiners[cycle_steiner[i]])
            pos2 = upscale(steiners[cycle_steiner[i+1]])
            pygame.draw.line(self.image, WHITE, pos1,pos2)
        pos1 = upscale(steiners[cycle_steiner[0]])
        pos2 = upscale(steiners[cycle_steiner[-1]])
        pygame.draw.line(self.image,WHITE,pos1,pos2)

        #draw the lines between the clients and the end offices
        (m,n) = C_client_target.shape
        for i in range(m) :
            for j in range(n):
                #regarder si le client est connecté au target
                if C_client_target[i,j]:
                    pos1 = upscale(clients[i])
                    pos2 = upscale(target_nodes[j])
                    pygame.draw.line(self.image, B,pos1, pos2)
        # draw the lines between target nodes and steiners
        (m,n) = C_target_steiner.shape
        for i in range(m):
            for j in range(n):
                if C_target_steiner[i,j]:
                    pos1 = upscale(target_nodes[i])
                    pos2 = upscale(steiners[j])
                    pygame.draw.line(self.image, G,pos1,pos2)







steiner = Steiner((150, 150))
end = EndOffices((300,300))
L = [steiner]
client = Clients((100,100))
# draw the steiners


from Telecom import TelecomEnv
from Agents import Solution
env = TelecomEnv()
environnement = env.reseau_telecom
agent = Solution(environnement)
links = Lines(agent,environnement)
while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                end.move_up()
                #steiner.rect.move_ip(0, -2)
            elif event.key == pygame.K_s:
                end.move_down()
                #steiner.rect.move_ip(0, 2)
            elif event.key == pygame.K_a:
                end.move_left()
                #steiner.rect.move_ip(-2, 0)
            elif event.key == pygame.K_d:
                end.move_right()
                #steiner.rect.move_ip(2, 0)

    bg = Background(env)
    screen.blit(bg.image, (0,0))
    screen.blit(links.image, (0,0))

    pygame.display.update()  # Or pygame.display.flip()


