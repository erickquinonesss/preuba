import pygame
from ajustes import *
from portada import toleportada
from menu import tolemenu
from fondo import FondoBase, FondoMontañas
from pajaro import Vuelo
from shot import Mirilla, handle_crosshair, crosshair_img
from colision import handle_collisions
from decision import toledecision
from creditos import Creditos
from rondas import RondasJuego
import sys

WHITE = (255, 255, 255)

class Scoref:
    def __init__(self, screen):
        self.screen = screen
        self.scoref_mostrados = False

    def mostrar_scoref(self):
        scoref = pygame.image.load('imagenes/scoref.jpg')
        self.screen.blit(scoref, (0, 0))
        pygame.display.flip()
        self.scoref_mostrados = True

class Juego:
    def __init__(self):
        pygame.init()
        self.Tamaño_pantalla = (WIDTH, HEIGHT)
        self.screen = pygame.display.set_mode(self.Tamaño_pantalla)
        pygame.display.set_caption(titulo)
        self.clock = pygame.time.Clock()
        self.juego_terminado = False
        self.creditos_mostrados = False
        self.start_time = None
        self.num_balas = 3
        self.score = 0
        self.mirilla = None
        self.vuelo = Vuelo(0, 600)
        self.moving_sprites = pygame.sprite.Group(self.vuelo)
        self.font = pygame.font.Font(None, 35)
        self.rondas_juego = RondasJuego(self.vuelo)  # Instancia de RondasJuego
        self.scoref = Scoref(self.screen)  # Instancia de Scoref

    def comprobar_fin_juego(self):
        if self.start_time is not None and pygame.time.get_ticks() - self.start_time > 8000:
            self.juego_terminado = True

    def mostrar_creditos(self):
        self.screen.blit(self.creditos, (0, 0))
        pygame.display.flip()
        self.creditos_mostrados = True

    def handle_shooting(self, event):
        global can_shoot, last_shot_time
        current_time = pygame.time.get_ticks()
        if event.type == pygame.MOUSEBUTTONDOWN and can_shoot:
            can_shoot = False
            last_shot_time = current_time
            print("Disparo registrado")
            mouse_pos = event.pos
            self.num_balas, self.score = handle_collisions(self.vuelo, self.moving_sprites, self.mirilla, self.num_balas, self.score, mouse_pos)
            self.mirilla.shoot()

        if current_time - last_shot_time > 500:  # Intervalo de medio segundo entre disparos
            can_shoot = True

    def mostrar_imagenes(self):
        # Mostrar la imagen de la ronda actual si corresponde
        self.rondas_juego.mostrar_ronda(self.screen)
        
        # Verificar si el contador de movimientos se reinicia
        if self.vuelo.obtener_contador_movimientos() == 4:
            print("Se ha completado una ronda. Reiniciando contador.")
            self.vuelo.contador_movimientos = 0
            self.rondas_juego.verificar_reinicio_contador()

    def run(self):
        mostrar_portada = toleportada(2)

        if mostrar_portada:
            iniciar_juego = tolemenu()

            if iniciar_juego:
                print("sisas")
                
                fondo = FondoBase()
                montañas = FondoMontañas()

                self.mirilla = Mirilla(crosshair_img)
                self.vuelo.movimiento()

                global can_shoot, last_shot_time
                can_shoot = True
                last_shot_time = 0

                self.start_time = pygame.time.get_ticks()

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        self.handle_shooting(event)

                    if self.juego_terminado:
                        if not self.scoref.scoref_mostrados:
                            self.scoref.mostrar_scoref()
                            pygame.time.wait(3000)  # Esperar 3 segundos para mostrar el score final

                        decision = toledecision()
                        if decision == "continuar":
                            self.juego_terminado = False
                            self.start_time = pygame.time.get_ticks()
                            self.scoref.scoref_mostrados = False  # Reiniciar para la próxima vez
                        elif decision == "creditos":
                            creditos = Creditos()
                            creditos.mostrar_creditos()
                            pygame.time.wait(5000)
                            pygame.quit()
                            sys.exit()
                        elif decision == "salir":
                            pygame.quit()
                            sys.exit()
                    else:
                        self.comprobar_fin_juego()
                        self.screen.fill(WHITE)
                        self.screen.blit(fondo.image, fondo.rect)

                        if self.vuelo.contador_movimientos % 6 < 3:
                            self.vuelo.volar_derecha(0.30)
                        else:
                            self.vuelo.volar_izquierda(0.30)

                        mouse_pos = pygame.mouse.get_pos()
                        handle_crosshair(self.num_balas, self.mirilla, self.screen)

                        if not self.vuelo.alive:
                            print("El pájaro ha sido derribado")
                            self.vuelo.caer(0.30)

                        self.moving_sprites.draw(self.screen)
                        self.moving_sprites.update(0.30)
                        
                        self.screen.blit(montañas.image, montañas.rect)
                        self.rondas_juego.mostrar_primera_ronda(self.screen)
                        
                        texto = f"{self.vuelo.contador_movimientos}/3"
                        texto_renderizado = self.font.render(texto, True, (255, 255, 255))
                        self.screen.blit(texto_renderizado, (365, 70))
                        
                        self.mostrar_imagenes()

                        pygame.display.update()

                    self.clock.tick(60)

if __name__ == "__main__":
    juego = Juego()
    juego.run()



