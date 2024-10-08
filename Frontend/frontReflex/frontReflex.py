"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
#from ...Fullstack.Backend.FastApi import  main
import requests as rq

from rxconfig import config


class Form_State(rx.State):
    """The app state."""

    form_data: dict
    clients:dict
    

    def handle_submit(self, form_data:list[dict]):
        """Handle the form submit."""
        #self.form_data=form_data
        self.form_data={"_id":"",
                        "username":form_data["username"],
                        "password":form_data["password"]
        }
        response = rq.request("get","https://coastal-blanche-gringos-ea9ebaeb.koyeb.app/users")
        #self.form_data = response  
        self.clients=response.json()


def index() -> rx.Component:
    # Welcome Page (Index)
    
         return rx.container(
            rx.form(
               rx.vstack(
                   #rx.input(name="id", type="hidden"),
                  rx.input(name="username", placeholder="Username", max_length=20),
                  rx.input(name="password", placeholder="Contraseña", type="password"),
                  rx.button("Submit", type="submit")           
                ),
                 on_submit=Form_State.handle_submit
               
            ),
            rx.text(Form_State.clients.to_string())
        
    )
   


app = rx.App()
app.add_page(index)
