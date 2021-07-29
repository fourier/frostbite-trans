import evnt

def trans(q1, q2):
    while True:
        ev = q2.get()
        if type(ev) == evnt.RequestTranslation:
            print("Translation requested")
            q1.put(evnt.SendTranslation(ev.text, "Перевод:" + ev.text ))
        else:
            print("Unknown event")
        
