import reflex as rx
#from ...Fullstack.Backend.FastApi import  main
import requests as rq
import json as js


from rxconfig import config


class State(rx.State):
    """The app state."""

    form_data_add: dict
    form_data_update: dict
    clients:list[dict]
    formAdd=True
    formUpdate=True
    button_submit:str
    neme_user:str
    eamil_user:str
    id_user:str
    clients_with_button:list[dict]
    

    def handle_submit_add(self, form_data_add:dict):
        """Handle the form submit."""
        #self.form_data_add=form_data
        self.form_data_add=js.dumps({"id":"", "username":form_data_add["username"], "email":form_data_add["email"]})
        print(form_data_add)
        response = rq.post("http://coastal-blanche-gringos-ea9ebaeb.koyeb.app/userdb",data=self.form_data_add)
        print(response)
        self.form_Add_not_hidden()
        self.get_clients_db()
       # self.clients=response.json()

    
    def handle_submit_Update(self, form_data_update:dict):
        """Handle the form submit."""
        #self.form_data_update=form_data
        self.form_data_update=js.dumps({"id":"", "username":"pepe", "email":form_data_update["email"]})
        print(self.form_data_update)
        print(form_data_update["id"])
        response = rq.put(f"http://coastal-blanche-gringos-ea9ebaeb.koyeb.app/userdb/",data=self.form_data_update)  
        print(response)
        #self.form_Update_not_hidden({})
        self.get_clients_db()
       # self.clients=response.json()
    


    

    #def clientsDB(rx.State):
        
    def get_clients_db(self):

         
         response = rq.get("http://coastal-blanche-gringos-ea9ebaeb.koyeb.app/userdb")
         self.clients= response.json() 
        

    
    def form_Add_not_hidden(self):
        self.formAdd=not self.formAdd
        
            
    def form_Update_not_hidden(self, person:dict ):
           # app.pages.get("formOculto").__setattr__("hidden", False)
        # print(person["username"])
         
        self.formUpdate=not self.formUpdate
        # rx.set_value("username",person["username"])
        # rx.set_value("email",person["email"])
        self.neme_user= person["username"]
        self.eamil_user= person["email"]
        self.id_user=person["id"]
            
         
         #if person is dict:
              #rx.set_value("id_colum",person["id"])
         

    def hundle_Buton_Delete(self, id: str):
          response = rq.delete("http://coastal-blanche-gringos-ea9ebaeb.koyeb.app/userdb/"+ id)
          print(response)
          self.get_clients_db()
  
    def clients_row_with_button(self, pos, val):
         for cwb in  self.clients:
            buttons= cwb.update({"ediar":rx.button(rx.icon(tag='pen')), "delete":rx.button(rx.icon(tag='trash'))})  
            self.clients_with_button.append(buttons) 
         print(self.clients)
         print(self.clients_with_button) 
         col, row=pos
         #rx.text(val[col][row])
         
         print(self.neme_user)
        # rx.set_value("email",person["email"]) 
    def set_name_user(self):
         self.neme_user=""
   
         

            
def show_person(person: dict):
    """Show a person in a table row."""
    return rx.table.row(
        rx.table.cell(person["id"], id="id_colum", name="id_colum" ),
        rx.table.cell(rx.text(person["username"], id="username_colum", disabled=True)),
        rx.table.cell(rx.text(person["email"], id="email_colum",disabled=True)),
        rx.button(rx.icon(tag="pen"),margin_left="1em", margin_rigth="2em", on_click=State.form_Update_not_hidden(person)),
        rx.button(rx.icon(tag="trash"), margin_left="1em", on_click=State.hundle_Buton_Delete(person["id"]))
        
    )

columns: list[dict[str, str]] = [
    {
        "title": "ID",
        "type": "str",
    },
    {
        "title": "Username",
        "type": "str",
    },
    {
        "title": "Email",
        "type": "str",
    }
]
data: list[list[dict]] = State.clients
def index() -> rx.Component:
    # Welcome Page (Index)
        return rx.container(
            rx.table.root(
              rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("ID"),
                        rx.table.column_header_cell("Userame"),
                        rx.table.column_header_cell("Email"),
                        
                     ),
                     
                ),
                
              rx.table.body(
                    rx.foreach(
                        State.clients , show_person
                   )
                ),
              on_mount= State.get_clients_db,
              width="100%"
            ),
            rx.button("Add", margin_top="2em", on_click=State.form_Add_not_hidden),
            rx.button("Delete", margin_top="2em",margin_left="1em"),
            #rx.button("Upgrade", margin_top="2em",margin_left="1em", on_click=State.form_Update_not_hidden),
            rx.container(
                rx.vstack(
                     rx.form(
                          rx.vstack(
                            rx.input(
                             name="username",
                             placeholder="Username",
                             #id="username",
                             
                            ),
                            rx.input(
                                name="email",
                                placeholder="Email",
                                #id="email",
                            ),
                
                            rx.button("Submit", type="submit"),
                        ),
                         on_submit=State.handle_submit_add,
                         reset_on_submit=True,
                         #id="formAddOculto",
                        hidden=State.formAdd
                     )
                ),
                rx.vstack(
                     rx.form(
                          rx.vstack(
                            rx.input(
                             value=State.neme_user,
                             placeholder="Username",
                             id="username",
                             name="username"
                             
                            ),
                         rx.input(value=State.eamil_user,
                                placeholder="Email",
                                id="email",
                                name="email"
                          ),
                          rx.input(value=State.id_user,
                                placeholder="Email",
                                id="id",
                                name="id"
                          ),
                
                     rx.button("SubmitUpdate", type="submit"),
                     ),
                    on_submit=State.handle_submit_Update,
                    reset_on_submit=True,
                    #id="formUpdateOculto",
                    hidden=State.formUpdate               
                    )
                 )

            ),
                 
            rx.data_editor(columns=columns,
                 data=data, 
                 on_cell_edited=State.clients_row_with_button,
            )
           
        )
    


app = rx.App()
app.add_page(index)
