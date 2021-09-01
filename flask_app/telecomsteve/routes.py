from flask import render_template, url_for, flash, redirect, request, session, abort 
from telecomsteve import app, db
# from telecomsteve.db_models import Contract, Peer, Host, Block
from telecomsteve.hackernews import Item, User, HackerNews
# from random import randint
# from datetime import datetime
import socket
import threading
import math

def get_host_ip():
    host_name = socket.gethostname() 
    host_ip = socket.gethostbyname(host_name) 
    return host_ip

def news_singleton(num):
    hn = HackerNews()
    stories = hn.top_stories()
    news_dict = {}
    try:
        website = hn.item(stories[num])
        news_dict[str(website.title)] = str(website.url)
    except:
        pass
    return(news_dict) 

@app.route("/")
def home():
    # if not session.get('logged_in'):
    #     return render_template('login_form.html', title='Login')

    if not session.get('logged_in'):
        return render_template('index.html')

    else:

        my_ip = get_host_ip()
        my_id = get_peer_id()
        peer_list_full = Peer.query.all()

        contract_page = request.args.get('contract_page', 1, type=int)
        contract_list = Contract.query.paginate(page=contract_page, per_page=3)
        contract_list_full = Contract.query.all()
        block_page = request.args.get('block_page', 1, type=int)
        block_list = Block.query.order_by(Block.time_stamp.desc()).paginate(page=block_page, per_page=5)

        return render_template('index.html')


@app.route("/news", methods=["GET"])
def news():
    count = range(50) # number of stories to display
    nthreads = 50 # number 

    def worker(count, outdict):
        """ The worker function, invoked in a thread. 'nums' is a
            list of numbers to factor. The results are placed in
            outdict.
        """
        for num in count:
            outdict[num] = news_singleton(num)

    # Each thread will get 'chunksize' nums and its own output dict
    chunksize = int(math.ceil(len(count) / float(nthreads)))
    threads = []
    outs = [{} for i in range(nthreads)]

    for i in range(nthreads):
        # Create each thread, passing it its chunk of numbers to factor
        # and output dict.
        t = threading.Thread(
                target=worker,
                args=(count[chunksize * i:chunksize * (i + 1)],
                      outs[i]))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Merge all partial output dicts into a single dict and return it
    output = ({k: v for out_d in outs for k, v in out_d.items()})

    return render_template('news.html', news=output)

@app.route("/portfolio")
def portfolio():
    return render_template('portfolio.html')

@app.route("/research")
def research():
    return render_template('research.html')

@app.route("/resume")
def resume():
    return render_template('resume.html')



# @app.route("/nodes", methods=["GET", "POST"])
# def nodes():

#     if request.method == "POST" and "peer_hostid" in request.form:

#         peer = request.form

#         new_peer = Peer(public_key=peer.get("peer_hostid"), ip=peer.get("peer_ip"), contract=peer.get("allowed_contract"))
#         db.session.add(new_peer)
#         db.session.commit()
#         print("this method is for a new peer")

#         return redirect(url_for('nodes'))

#     elif request.method == "POST" and "tps" in request.form:

#         print("this method is for benchmarking")

#         return redirect(url_for('nodes'))
    
#     else:
#         my_ip = get_host_ip()
#         my_id = get_peer_id()
#         peer_page = request.args.get('peer_page', 1, type=int)
#         peer_list = Peer.query.paginate(page=peer_page, per_page=10)
#         peer_list_full = Peer.query.all()
#         contract_list = Contract.query.all()

#         return render_template('nodes.html', title='Nodes', about=about, ip=my_ip, id=my_id, peers=peer_list, peers_full=peer_list_full, contracts_full=contract_list, peer_page=peer_page)

@app.route("/login", methods=['POST'])
def login():
    if request.form['password'] == 'spectrum' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()
