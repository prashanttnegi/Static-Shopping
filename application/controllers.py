from flask import Flask,request,redirect
from flask import render_template,send_file
from flask import current_app as app
from PIL import Image as PILImage
import io
from io import BytesIO
from application.models import *
from .models import db
import bcrypt
import matplotlib.pyplot as plt


@app.route("/", methods=['GET','POST'])
def home():
    try:
        id = int(request.args.get('user'))
        user=User.query.get(id)
        categories=Category.query.all()
        return render_template('home.html', user=user,categories=categories)
    except:
        categories=Category.query.all()       
        return render_template('home.html',user='',categories=categories)
    

@app.route("/admin_login", methods=['GET','POST'])
def ad_login():
    if request.method == 'POST':
      try:
        user_id = request.form.get('email')
        password=request.form.get('password')
        
        user=Admin.query.filter_by(admin_id=user_id).first()
        if user.password==password:    
            user.active=1
            status="active"
            db.session.commit()
            return redirect("/dashboard/"+str(user.id))
        else:
            return render_template('admin_login.html',error='Wrong Password! Try again.')
      except:
        return render_template('admin_login.html', error="Not registered with this email!")
    if request.method=='GET':
        return render_template('admin_login.html')
    
@app.route("/admin_logout/<int:id>", methods=['GET','POST'])
def ad_logout(id):
    user=Admin.query.get(id)
    user.active=0
    db.session.commit()
    return redirect('/admin_login')

@app.route("/dashboard/<int:id>", methods=['GET','POST'])
def dashboard(id):
    user = Admin.query.get(id)
    categories=Category.query.all()
    return render_template("admin_dashboard.html",user=user,categories=categories)

@app.route("/user_login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
      try:
        user_id = request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email_id=user_id).first()
        stored_hashed_password=user.password
        if bcrypt.checkpw(password.encode('utf-8'),stored_hashed_password):    
            user.active=1
            db.session.commit()
            return redirect('/?user=' + str(user.id))
        else:
            return render_template('user_login.html',error='Wrong Password! Try again.')
      except:
        return render_template('user_login.html', error="Not registered with this email. Please register first!")
    if request.method=='GET':
        return render_template('user_login.html')

@app.route("/logout/<int:id>",methods=['GET','POST'])
def logout(id):
    user=User.query.get(id)
    user.active=0
    db.session.commit()
    return redirect('/')

@app.route("/register",methods=['GET','POST'])
def reg():
    if request.method=='GET':
        return render_template('register.html')
    if request.method=='POST':
        try:
            email=request.form.get('email')
            password=request.form.get('password')
            encrypted_password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
            r1=User(email_id=email,password=encrypted_password)
            db.session.add(r1)
            db.session.commit()
            return redirect('/user_login')
        except:
            return render_template('register.html',error='Email already registered. Try logging in or registering using different email_id.')
        
@app.route("/profile/<int:id>",methods=['GET','POST'])
def profile(id):
    user=User.query.get(id)
    orders=Orders.query.filter_by(user_id=id).all()
    all_orders=[]
    count=0
    total=[]
    if orders:
        all_orders.append([orders[0]])
        total.append(orders[0].total)
        for i in range(1,len(orders)):
            if orders[i].order_id == all_orders[count][0].order_id:
                all_orders[count].append(orders[i])
                total[count]+=orders[i].total
                
            else:
                count+=1
                all_orders.append([])
                total.append(0)
                all_orders[count].append(orders[i])
                total[count]+=orders[i].total
                
    return render_template('profile.html',user=user,total=total,orders=all_orders)

@app.route("/about")
def about():
    id = request.args.get('user')
    if id==str(1):
        user=Admin.query.get(id)
        return render_template('about.html',user=user)
    if id:
        user=User.query.get(id)
        return render_template('about.html',user=user)
    
    return render_template('about.html',user='')

@app.route("/delete_user/<int:id>",methods=['GET','POST'])
def delete_user(id):
    user=User.query.get(id)
    cart=Cart.query.filter_by(user_id=id).all()
    if user.cart:
        for products in user.cart:
            db.session.delete(products)
    db.session.delete(user)
    db.session.commit()
    return redirect('/user_login')

@app.route("/add_category/<int:id>", methods=['GET','POST'])
def add_category(id):
    if request.method=='GET':
        user=Admin.query.get(id)
        return render_template("add_category.html",user=user)
    if request.method=='POST':
        name=request.form.get('name')
        description=request.form.get('description')
        image_file = request.files['image']

        # Read the image file and convert it to binary data
        pil_image = PILImage.open(image_file)
        rgb_img = pil_image.convert('RGB')
        image_data = io.BytesIO()
        rgb_img.save(image_data, format='JPEG')
        image_data = image_data.getvalue()

        c1=Category(name=name,description=description,image=image_data)
        db.session.add(c1)
        db.session.commit()
        return redirect('/dashboard/'+str(id))
    
@app.route("/edit_category/<int:id>/<int:c_id>", methods=['GET','POST'])
def edit_cat(id,c_id):
    if request.method=='GET':
        cat=Category.query.get(c_id)
        user=Admin.query.get(id)
        return render_template("edit_category.html",user=user,category=cat)
    if request.method=='POST':
        cat=Category.query.get(c_id)
        name=request.form.get('name')
        description=request.form.get('description')
        if name:
            cat.name=name
        if description:
            cat.description=description
    
        image_file = request.files['image']
        
        if image_file:
            pil_image = PILImage.open(image_file)
            rgb_img = pil_image.convert('RGB')
            image_data = io.BytesIO()
            rgb_img.save(image_data, format='JPEG')
            image_data = image_data.getvalue()
            cat.image = image_data
        db.session.commit()
        return redirect('/dashboard/'+str(id))
        
@app.route("/delete_category/<int:id>/<int:c_id>", methods=['GET','POST'])
def delete_cat(id,c_id):
    user=User.query.get(id)
    cat=Category.query.get(c_id)
    products=cat.products
    for product in products:
        db.session.delete(product)
    db.session.delete(cat)
    db.session.commit()
    return redirect('/dashboard/'+str(id))
    
    
@app.route('/image/<int:category_id>')
def display_image_category(category_id):
    category = Category.query.get(category_id)
    if category and category.image:
        return send_file(BytesIO(category.image), mimetype='image/jpeg')
    return 'Image not found'

@app.route('/add_product/<int:id>/<int:c_id>', methods=['GET','POST'])
def create_product(id,c_id):
    if request.method=='GET':
        user=Admin.query.get(id)
        category=Category.query.get(c_id)
        units=Units.query.all()
        return render_template('add_product.html',user=user,category=category,units=units)
    if request.method=='POST':
        user=Admin.query.get(id)
        category=Category.query.get(c_id)
        category_id=c_id
        product_name=request.form.get('name')
        unit_id=request.form.get("unit")
        unit=Units.query.get(int(unit_id)).name
        rate=request.form.get('rate')
        quantity=request.form.get('quantity')
        image_file = request.files['image']
        pil_image = PILImage.open(image_file)
        rgb_img = pil_image.convert('RGB')
        image_data = io.BytesIO()
        rgb_img.save(image_data, format='JPEG')
        image_data = image_data.getvalue()
        p1=Products(category_id=category_id,product_name=product_name,unit=unit,rate=rate,quantity=quantity,image=image_data)
        db.session.add(p1)
        db.session.commit()
        return redirect('/dashboard/'+str(id))
    
@app.route('/product_edit/<int:id>/<int:p_id>', methods=['GET','POST'])
def prod_edit(id,p_id):
    if request.method=='GET':
        prod=Products.query.get(p_id)
        user=Admin.query.get(id)
        categories=Category.query.all()
        return render_template("edit_product.html",user=user,product=prod,categories=categories)
    if request.method=='POST':
        prod=Products.query.get(p_id)
        name=request.form.get('name')
        category=request.form.get('category')
        rate=request.form.get('rate')
        quantity=request.form.get('quantity')
        if name:
            prod.product_name=name
        if rate:
            prod.rate=rate
        if quantity:
            prod.quantity=quantity
        if category is not None:
            prod.category_id=category
            
        checkbox_value = request.form.get("readCheckbox")
        if checkbox_value == "on":    
            image_file = request.files['image']
            pil_image = PILImage.open(image_file)
            rgb_img = pil_image.convert('RGB')
            image_data = io.BytesIO()
            rgb_img.save(image_data, format='JPEG')
            image_data = image_data.getvalue()
            prod.image=image_data
        
        db.session.commit()
        return redirect('/dashboard/'+str(id))
    
@app.route("/product_delete/<int:id>/<int:p_id>")
def prod_delete(id,p_id):
    user=User.query.get(id)
    prod=Products.query.get(p_id)
    items=prod.cart
    for item in items:
        db.session.delete(item)
    db.session.delete(prod)
    db.session.commit()
    return redirect('/dashboard/'+str(id))
    
@app.route('/image_product/<int:product_id>')
def display_image_product(product_id):
    product = Products.query.get(product_id)
    if product and product.image:
        return send_file(BytesIO(product.image), mimetype='image/jpeg')
    return 'Image not found'

@app.route('/add_cart/<int:id>/<int:p_id>',methods=['GET','POST'])
def add_cart(id,p_id):
    if request.method=='GET':
        user=User.query.get(id)
        product=Products.query.get(p_id)
        error = str(request.args.get('error'))
        if error=='1':
            error="Entered quantity is greater than the available quantity"
            return render_template('add_to_cart.html',user=user,product=product,error=error)
        else:           
            return render_template('add_to_cart.html',user=user,product=product)
    if request.method=='POST':
        user=User.query.get(id)
        product=Products.query.get(p_id)
        product_id=product.id
        rate=product.rate
        quantity=request.form.get('quantity')
        product_quantity=product.quantity        
        if float(quantity)>product_quantity:
            return redirect('/add_cart/'+str(id)+'/'+str(product_id)+'?error=' + str(1))
        else:
            total=float(quantity)*int(rate)
            c1=Cart(user_id=id,product_id=product_id,quantity=quantity,total=total)
            db.session.add(c1)
            db.session.commit()
        return redirect('/?user=' + str(user.id))
    
    
@app.route('/cart/<int:id>',methods=['GET'])
def user_cart(id):
    if request.method=='GET':
        user=User.query.get(id)
        cart=Cart.query.filter_by(user_id=id).all()
        new_cart=cart.copy()
        total=0
        out_of_stock=[]
        for el in cart:
            if el.product.quantity<el.quantity:
                out_of_stock.append(el)
                new_cart.remove(el)
            else:
                total+=el.total
        return render_template('user_cart.html',user=user,cart=new_cart,total=total,out_of_stock=out_of_stock)

@app.route('/delete_item/<int:id>/<int:p_id>',methods=['GET','POST'])
def delete_item(id,p_id):
    user=User.query.get(id)
    cart=Cart.query.get(p_id)
    db.session.delete(cart)
    db.session.commit()
    return redirect('/cart/'+str(id))

@app.route('/checkout/<int:id>',methods=['GET','POST'])
def checkout(id):
    user=User.query.get(id)
    cart=Cart.query.filter_by(user_id=id).all()
    new_cart=cart.copy()
    total=0
    order_id=Orders.query.all()
    if order_id:
        order_id=Orders.query.all()[-1].order_id+1
    else:
        order_id=1
    out_of_stock=[]
    for el in cart:
        if el.product.quantity<el.quantity:
            out_of_stock.append(el)
            new_cart.remove(el)
        else:
            pass

    for i in new_cart:
        o1=Orders(order_id=order_id,user_id=id,category_name=i.product.category.name,product_name=i.product.product_name,quantity=str(i.quantity)+i.product.unit.split('/')[-1],rate=str(i.product.rate)+i.product.unit,total=i.total)
        db.session.add(o1)
        i.product.quantity-=float(i.quantity)
        total+=i.total
        db.session.delete(i)
    db.session.commit()
    return render_template('checkout.html',user=user,cart=new_cart,rejected_cart=out_of_stock,total=total)

@app.route('/search/<int:id>',methods=['GET','POST'])
def search(id):
    user=User.query.get(id)
    searched = str(request.args.get('query'))
    categories=Category.query.filter(Category.name.like(f'%{searched}%')).all()
    products=Products.query.filter(Products.product_name.like(f'%{searched}%')).all()
    if categories:
        return render_template('search.html',user=user,item="category",categories=categories)
    if products:
        return render_template('search.html',user=user,item="product",products=products)
    else:
        return render_template('search.html',user=user,error="No results found")

@app.route('/inventory/<int:id>',methods=['GET','POST'])
def inventory(id):
    user=Admin.query.get(id)
    products=Products.query.all()
    return render_template('inventory.html',user=user,products=products)

@app.route('/summary/<int:id>',methods=['GET','POST'])
def summary(id):
    user=Admin.query.get(id)
    categories=Category.query.all()
    names=[]
    quantities=[]
    for category in categories:
        if category.name not in names:
            names.append(category.name)
        else:
            pass
        quantities.append(len(category.products))

    orders=Orders.query.all()
    
    products={}
    
    for item in orders:
        if item.product_name  not in products.keys():
            quantity=int((item.quantity[0]) + item.quantity[1] if item.quantity[1].isdigit() else item.quantity[0])
            products[item.product_name]=quantity
        else:
            quantity=int((item.quantity[0]) + item.quantity[1] if item.quantity[1].isdigit() else item.quantity[0])
            products[item.product_name]+=quantity
            
    products=dict(sorted(products.items(), key=lambda x: x[1], reverse=True))
    
    plt.figure(figsize=(7, 5))
    plt.bar(names,quantities)
    plt.xlabel('Categories',fontsize=12)
    plt.ylabel('No. of Products',fontsize=12)
    plt.title('Category-wise products', fontsize=16)
    cat_wise_prod = "static/graph.png"
    plt.savefig(cat_wise_prod)

    plt.figure(figsize=(7, 5))
    plt.bar(list(products.keys())[:5],list(products.values())[:5])
    plt.xlabel('Products',fontsize=12)
    plt.ylabel('Sales Unit',fontsize=12)
    plt.title('Top-5 selling Products',fontsize=16)
    cat_wise_prod_2 = "static/graph_2.png"
    plt.savefig(cat_wise_prod_2)
    
    return render_template('summary.html',user=user,cat_wise_graph=cat_wise_prod,cat_wise_graph_2=cat_wise_prod_2)