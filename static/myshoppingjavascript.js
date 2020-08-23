function adminlogin() {
    if ($('#frm_admin').valid()) {
        var email = document.getElementById('email').value;
        var password = document.getElementById('password').value;
        var formdata = new FormData();
        formdata.append('email', email);
        formdata.append('password', password);
        var xml = new XMLHttpRequest();
        xml.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var ar = JSON.parse(this.response);
                if (ar['message'] == "Login Success") {
                    window.location.href = "AdminHomePage";
                }
                else {
                    document.getElementById('sp1').innerHTML = ar['message'];
                }
            }
        };
        xml.open('POST', 'adminloginaction', true);
        xml.send(formdata);
    }
    ;
}

function addadmin() {
    if ($('#frm_insertrecord').valid()) {
        var email = document.getElementById('textbox1').value;
        var password = document.getElementById('textbox2').value;
        var fullname = document.getElementById('textbox3').value;
        var admintype = document.getElementById('textbox4').value;
        var xml = new XMLHttpRequest();
        xml.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var ar = JSON.parse(this.response);
                document.getElementById('sp1').innerHTML = ar['message'];
                document.getElementById('textbox1').value = '';
                document.getElementById('textbox2').value = '';
                document.getElementById('textbox3').value = '';
                document.getElementById('textbox4').value = 'Sub Admin';
            }
        };
        xml.open('GET', 'InsertRecord?email=' + email + '&password=' + password + '&fullname=' + fullname + '&admintype=' + admintype, true);
        xml.send();
    }
    ;
}

function changepassword() {
    if ($('#frm_insertrecord').valid()) {
        var password = document.getElementById('password').value;
        var newpassword = document.getElementById('newpassword').value;
        var formdata = new FormData();
        formdata.append('password', password);
        formdata.append('newpassword', newpassword);
        var xml = new XMLHttpRequest();
        xml.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var ar = JSON.parse(this.response);
                if (ar['message'] == "Wrong Password") {
                    document.getElementById('password').value = '';
                    document.getElementById('sp1').innerHTML = ar['message'];
                }
                else {
                    window.location.href = "AdminHomePage";
                }
            }
        };
        xml.open('POST', 'OnClickChangePassword', true);
        xml.send(formdata);
    }
    ;
}

function pendingorders() {
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var ar = JSON.parse(this.response);
            var s = "";
            s += "<table class='table text-center'>";
            s += "<tr>";
            s += "<th class='text-center'>" + 'ORDER ID' + "</th>";
            s += "<th class='text-center'>" + 'DATE' + "</th>";
            s += "<th class='text-center'>" + 'EMAIL' + "</th>";
            s += "<th class='text-center'>" + 'NAME' + "</th>";
            s += "<th class='text-center'>" + 'MOBILENO' + "</th>";
            s += "<th class='text-center'>" + 'CITY' + "</th>";
            s += "<th class='text-center'>" + 'AMOUNT' + "</th>";
            s += "<th class='text-center'>" + 'PAYMENT MODE' + "</th>";
            s += "<th class='text-center'>" + 'ACCEPT' + "</th>";
            s += "<th class='text-center'>" + 'REJECT' + "</th>";
            s += "</tr>";
            for (var i = 0; i < ar.length; i++) {
                s += "<tr>";
                s += "<td>" + ar[i]['id'] + "</td>";
                s += "<td>" + ar[i]['dateoforder'] + "</td>";
                s += "<td>" + ar[i]['email'] + "</td>";
                s += "<td>" + ar[i]['fullname'] + "</td>";
                s += "<td>" + ar[i]['mobileno'] + "</td>";
                s += "<td>" + ar[i]['city'] + "</td>";
                s += "<td>" + ar[i]['netamount'] + "</td>";
                s += "<td>" + ar[i]['paymentmode'] + "</td>";
                s += "<td class='text-center'><button class='btn btn-success' onclick=approve_reject_order(" + ar[i]['id'] + ",'Accepted'," + ar[i]['mobileno'] + ")>ACCEPT</button></td>";
                s += "<td class='text-center'><button class='btn btn-danger' onclick=approve_reject_order(" + ar[i]['id'] + ",'Rejected'," + ar[i]['mobileno'] + ")>REJECT</button></td>";
                s += "</tr>";
            }
            s += "</table>";
            document.getElementById('output').innerHTML = s;
        }
    };
    xml.open('GET', 'pendingordersaction', true);
    xml.send();
}

function approve_reject_order(orderid, status, mobileno) {
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var ar = JSON.parse(this.response);
            window.location.href = "pendingorderpage";
        }
    };
    xml.open('GET', 'approve_reject_action?orderid=' + orderid + '&status=' + status + '&mobileno=' + mobileno, true);
    xml.send();
}

function changeuserpassword() {
    if ($('#frm_insertrecord').valid()) {
        var password = document.getElementById('password').value;
        var newpassword = document.getElementById('newpassword').value;
        var formdata = new FormData();
        formdata.append('password', password);
        formdata.append('newpassword', newpassword);
        var xml = new XMLHttpRequest();
        xml.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var ar = JSON.parse(this.response);
                if (ar['message'] == "Wrong Password") {
                    document.getElementById('password').value = '';
                    document.getElementById('sp1').innerHTML = ar['message'];
                }
                else {
                    window.location.href = "index";
                }
            }
        };
        xml.open('POST', 'OnClickChangeUserPassword', true);
        xml.send(formdata);
    }
    ;
}

function edituserprofile() {
    if ($('#frm_edituserprofile').valid()) {
        var fullname = (document.getElementById('fullname').value);
        fullname = fullname.replace(/\s+/g, ' ').trim();
        var phoneno = document.getElementById('phoneno').value;
        var address = document.getElementById('address').value;
        var city = document.getElementById('city').value;
        var formdata = new FormData();
        formdata.append('fullname', fullname);
        formdata.append('phoneno', phoneno);
        formdata.append('address', address);
        formdata.append('city', city);
        var xml = new XMLHttpRequest();
        xml.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var ar = JSON.parse(this.response);
                document.getElementById('sp11').innerHTML = ar['message'];
            }
        };
        xml.open('POST', 'OnClickChangeUserName', true);
        xml.send(formdata);
    }
    ;
}

function myorders(useremail) {
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var ar = JSON.parse(this.response);
            if (ar['message'] == 'No Product Ordered') {
                document.getElementById('outputordered').innerText = ar['message'];
            }
            else {
                var s = "";
                s += "<table class='table text-center table-hover'>";
                s += "<tr>";
                s += "<th class='text-center'>" + 'ORDER ID' + "</th>";
                s += "<th class='text-center'>" + 'DATE' + "</th>";
                s += "<th class='text-center'>" + 'NAME' + "</th>";
                s += "<th class='text-center'>" + 'MOBILENO' + "</th>";
                s += "<th class='text-center'>" + 'CITY' + "</th>";
                s += "<th class='text-center'>" + 'AMOUNT' + "</th>";
                s += "<th class='text-center'>" + 'STATUS' + "</th>";
                s += "<th class='text-center'>" + 'PAYMENT MODE' + "</th>";
                s += "</tr>";
                for (var i = 0; i < ar.length; i++) {
                    s += "<tr>";
                    s += "<td>" + ar[i]['id'] + "</td>";
                    s += "<td>" + ar[i]['dateoforder'] + "</td>";
                    s += "<td>" + ar[i]['fullname'] + "</td>";
                    s += "<td>" + ar[i]['mobileno'] + "</td>";
                    s += "<td>" + ar[i]['city'] + "</td>";
                    s += "<td>" + ar[i]['netamount'] + "</td>";
                    s += "<td>" + ar[i]['status'] + "</td>";
                    s += "<td>" + ar[i]['paymentmode'] + "</td>";
                    s += "</tr>";
                }
                s += "</table>";
                document.getElementById('output').innerHTML = s;
            }
        }
    };
    xml.open('GET', 'myordersaction?email=' + useremail, true);
    xml.send();
}

function OnInsertClick() {
    if ($('#frm_insert').valid()) {
        var category = document.getElementById('Textbox1').value;
        var description = document.getElementById('Textbox2').value;
        var xml = new XMLHttpRequest();
        xml.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var ar = JSON.parse(this.response);
                document.getElementById('sp1').innerHTML = ar['message'];
                document.getElementById('Textbox1').value = '';
                document.getElementById('Textbox2').value = '';
            }
        };
        xml.open('GET', 'OnClickInsertCT?category=' + category + '&description=' + description, true);
        xml.send();
    }
    ;
}

function addproduct() {
    if ($('#frm_addproduct').valid()) {
        var formdata = new FormData();
        formdata.append('categoryname', document.getElementById('categoryname').value);
        formdata.append('pname', document.getElementById('pname').value);
        formdata.append('price', document.getElementById('price').value);
        formdata.append('mrp', document.getElementById('mrp').value);
        formdata.append('description', document.getElementById('description').value);
        formdata.append('photo', document.getElementById('photo').files[0]);
        var xml = new XMLHttpRequest();
        xml.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var ar = JSON.parse(this.response);
                document.getElementById('sp1').value = ar["message"];
                document.getElementById('categoryname').value = '';
                document.getElementById('pname').value = '';
                document.getElementById('description').value = '';
                document.getElementById('price').value = '';
                document.getElementById('mrp').value = '';
                document.getElementById('photo').value = '';
            }
        };
        xml.open('POST', 'addproductaction', true);
        xml.send(formdata);
    }
    ;
}

function viewproduct() {
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var ar = JSON.parse(this.response);
            var s = "";
            s += "<table class='table table-striped'>";
            s += "<tr>";
            s += "<th class='text-center'>" + 'Product ID' + "</th>";
            s += "<th class='text-center'>" + 'Product Name' + "</th>";
            s += "<th class='text-center'>" + 'Description' + "</th>";
            s += "<th class='text-center'>" + 'Price' + "</th>";
            s += "<th class='text-center'>" + 'MRP' + "</th>";
            s += "<th class='text-center'>" + 'Picture Name' + "</th>";
            s += "<th class='text-center'>" + 'Category' + "</th>";
            s += "<th class='text-center'>" + 'Picture' + "</th>";
            s += "<th class='text-center'>" + 'Edit' + "</th>";
            s += "<th class='text-center'>" + 'Delete' + "</th>";
            s += "</tr>";
            for (var i = 1; i < ar.length; i++) {
                s += "<tr>";
                s += "<td>" + ar[i]['pid'] + "</td>";
                s += "<td>" + ar[i]['pname'] + "</td>";
                s += "<td>" + ar[i]['description'] + "</td>";
                s += "<td>" + ar[i]['price'] + "</td>";
                s += "<td>" + ar[i]['mrp'] + "</td>";
                s += "<td>" + ar[i]['photo'] + "</td>";
                s += "<td>" + ar[i]['categoryname'] + "</td>";
                s += "<td><img src='../static/media/" + ar[i]['photo'] + "' style='width: 70px; height:60px;'></td>";
                s += "<td class='text-center'><a href='editproductpage?pid=" + ar[i]['pid'] + "'><span class='glyphicon glyphicon-pencil'></span></a></td>";
                s += "<td class='text-center'><a href='deleteproductaction?pid=" + ar[i]['pid'] + "'><span class='glyphicon glyphicon-trash' style='color: red'></span></a></td>";
                s += "</tr>";
            }
            s += "</table>";
            document.getElementById('output').innerHTML = s;
        }
    };
    xml.open('GET', 'viewproductaction', true);
    xml.send();
}

function viewallproducts() {
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var ar = JSON.parse(this.response);
            var s = "<div class='row'>";
            for (var i = 0; i < ar.length; i++) {
                s += "<div class='col-md-3 product-men women_two'>";
                s += "<div class='product-toys-info' style='background-color: white'>";
                s += "<div class='men-pro-item'>";
                s += "<div class='men-thumb-item'>";
                s += "<div><img class='img-responsive' src='../static/media/" + ar[i]['photo'] + "' style='width: 600px; height: 200px'></div>";
                s += "<div class='men-cart-pro'>";
                s += "<div class='inner-men-cart-pro'>";
                s += "<button style='border: 0px; border-radius: 20px' class='link-product-add-cart' onclick='quickview(" + ar[i]['pid'] + ")'>Quick View</button>";
                s += "</div>";
                s += "</div>";
                s += "<span class='product-new-top'>New</span>";
                s += "</div>";
                s += "<div class='item-info-product'>";
                s += "<div class='info-product-price'>";
                s += "<div class='grid_meta'>";
                s += "<div class='product_price'>";
                s += "<h4 class='text-center'>" + ar[i]['pname'] + "</h4>";
                s += "<div class='grid-price mt-2'>";
                s += "<div class='text-center'><span class='money' style='color: blue;'>₹ " + ar[i]['price'] + "</span><del style='color: red;'>₹ " + ar[i]['mrp'] + "</del></div>";
                s += "</div>";
                s += "</div>";
                s += "</div>";
                s += "</div>";
                s += "<div class='toys single-item hvr-outline-out'>";
                s += "<button type='button' class='toys-cart ptoys-cart btn btn-success' style='margin-top: -10px' onclick='addtocart(" + ar[i]['pid'] + "," + ar[i]['price'] + ")'><i class='fas fa-cart-plus'></i></button>";
                s += "</div>";
                s += "</div>";
                s += "</div>";
                s += "</div>";
                s += "</div>";
            }
            document.getElementById('output').innerHTML = s;
        }
    };
    xml.open('GET', 'showallproductaction', true);
    xml.send();
}

function usersignup() {
    if ($('#frm_usersignup').valid()) {
        var fullname = document.getElementById('fullname').value;
        var mobileno = document.getElementById('mobileno').value;
        var address = document.getElementById('address').value;
        var city = document.getElementById('city').value;
        var uemail = document.getElementById('uemail').value;
        var upassword = document.getElementById('upassword').value;
        // var confirmpassword = document.getElementById('confirmpassword').value;
        var xml = new XMLHttpRequest();
        xml.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var ar = JSON.parse(this.response);
                if (ar['message'] == "Data saved") {
                    window.location.href = "index";
                }
                else {
                    document.getElementById('uemail').value = '';
                    document.getElementById('sp1').innerHTML = 'Email Already Used';
                }
            }
        };
        xml.open('GET', 'usersignupaction?fullname=' + fullname + '&mobileno=' + mobileno + '&address=' + address + '&city=' + city + '&uemail=' + uemail + '&upassword=' + upassword, true);
        xml.send();
    }
}

function userlogin() {
    if ($('#frm_usersignin').valid()) {
        var email = document.getElementById('email').value;
        var password = document.getElementById('password').value;
        var formdata = new FormData();
        formdata.append('email', email);
        formdata.append('password', password);
        var xml = new XMLHttpRequest();
        xml.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var ar = JSON.parse(this.response);
                if (ar['message'] == "Login Success") {
                    window.location.href = "index";
                }
                else {
                    document.getElementById('sp11').innerHTML = ar['message'];
                }
            }
        };
        xml.open('POST', 'userloginaction', true);
        xml.send(formdata);
    }
}

function addtocart(pid, price) {
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var ar = JSON.parse(this.response);
            alert("1 element added to cart");
        }
    };
    xml.open('GET', 'addtocartaction?pid=' + pid + '&price=' + price, true);
    xml.send();
}

function addtocartquickview(pid, price) {
    var qty = document.getElementById('qty').value;
    var price = price;
    var amount = price * qty;
    var pid = pid;
    var formdata = new FormData();
    formdata.append('pid', pid);
    formdata.append('qty', qty);
    formdata.append('amount', amount);
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var ar = JSON.parse(this.response);
            alert(qty + " element(s) added to cart");
            document.getElementById('qty').value = 1;

        }
    };
    xml.open('POST', 'addtocartquickviewaction', true);
    xml.send(formdata);
}

function quickview(pid) {
    window.location.href = "single?pid=" + pid;
}

function mycart() {
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var ar = JSON.parse(this.response);
            if (ar['message'] != 'No Product') {
                var s = "";
                var netamount = 0;
                s += "<table class='table table-bordered'>";
                s += "<tr>";
                s += "<th class='text-center'>" + 'Serial Number' + "</th>";
                s += "<th class='text-center'>" + 'Product Name' + "</th>";
                s += "<th class='text-center'>" + 'Picture' + "</th>";
                s += "<th class='text-center'>" + 'Price' + "</th>";
                s += "<th class='text-center'>" + 'QTY' + "</th>";
                s += "<th class='text-center'>" + 'Amount' + "</th>";
                s += "</tr>";
                for (var i = 0; i < ar.length; i++) {
                    netamount += parseFloat(ar[i]['amount']);
                    s += "<tr>";
                    s += "<td>" + [i + 1] + "</td>";
                    s += "<td>" + ar[i]['pname'] + "</td>";
                    s += "<td><img src='../static/media/" + ar[i]['photo'] + "' style='width: 70px; height: 60px'></td>";
                    s += "<td>" + ar[i]['price'] + "</td>";
                    s += "<td>" + ar[i]['qty'] + "</td>";
                    s += "<td>" + ar[i]['amount'] + "</td>";
                    s += "</tr>";
                }
                s += "<tr>";
                s += "<td colspan='5' class='text-right'><strong>Net Amount</strong>";
                s += "<td><strong>" + netamount + "</strong></td>";
                s += "<tr>";
                s += "<td colspan=6 class='text-center'><a href='shop' class='btn btn-warning'>Continue Shopping</a>&nbsp;&nbsp;<a href='proceedtopay' class='btn btn-success'>Proceed To Pay</a></td>";
                s += "</tr>";
                s += "</tr>";
                s += "</table>";
                document.getElementById('output').innerHTML = s;
            }
            else {
                document.getElementById('outputnoele').innerHTML = 'No Product in Cart';
            }
        }
    };
    xml.open('GET', 'mycartaction', true);
    xml.send();
}

function cont() {
    if ($('#frm_cont').valid()) {
        var name = document.getElementById('name').value;
        var email = document.getElementById('email').value;
        var phoneno = document.getElementById('phoneno').value;
        var content = document.getElementById('content').value;
        var formdata = new FormData();
        formdata.append('name', name);
        formdata.append('email', email);
        formdata.append('phoneno', phoneno);
        formdata.append('content', content);
        var xml = new XMLHttpRequest();
        xml.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var ar = JSON.parse(this.response);
                document.getElementById('sp1').innerHTML = ar['message'];
                document.getElementById('name').value = '';
                document.getElementById('email').value = '';
                document.getElementById('phoneno').value = '';
                document.getElementById('content').value = '';
            }
        };
        xml.open('POST', 'contentaction', true);
        xml.send(formdata);
    }
}

function reviewaction(pid) {
    if ($('#review').valid()) {
        var pid = pid;
        var email = document.getElementById('email').value;
        var content = document.getElementById('content').value;
        var formdata = new FormData();
        formdata.append('pid', pid);
        formdata.append('email', email);
        formdata.append('content', content);
        var xml = new XMLHttpRequest();
        xml.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var ar = JSON.parse(this.response);
                document.getElementById('sp1').innerHTML = ar['message'];
                document.getElementById('email').value = '';
                document.getElementById('content').value = '';
            }
        };
        xml.open('POST', 'reviews', true);
        xml.send(formdata);
    }
}

function show() {
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var ar = JSON.parse(this.response);
            var s = "<div class='row'>";
            for (var i = 0; i < 8; i++) {
                s += "<div class='col-md-3 product-men women_two'>";
                s += "<div class='product-toys-info' style='background-color: white'>";
                s += "<div class='men-thumb-item'>";
                s += "<div><img class='img-responsive' src='../static/media/" + ar[i]['photo'] + "' style='width: 100%; height: 200px'></div>";
                s += "<div class='men-cart-pro'><div class='inner-men-cart-pro'><button style='border: 0px; border-radius: 20px' class='link-product-add-cart' onclick='quickview(" + ar[i]['pid'] + ")'>Quick View</button></div></div>";
                s += "<span class='product-new-top'>New</span>";
                s += "<div class='info-product-price'><h4 class='text-center'>" + ar[i]['pname'] + "</h4></div>";
                s += "</div>";
                s += "</div>";
                s += "</div>";
            }
            s += "</div>";
            document.getElementById('output').innerHTML = s;
        }
    };
    xml.open('GET', 'showaction', true);
    xml.send();
}

function viewcat(cat) {
    var cat = cat;
    var formdata = new FormData();
    formdata.append('cat', cat);
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var ar = JSON.parse(this.response);
            var s = "<div class='row'>";
            for (var i = 0; i < ar.length; i++) {
                s += "<div class='col-md-3 product-men women_two'>";
                s += "<div class='product-toys-info' style='background-color: white'>";
                s += "<div class='men-pro-item'>";
                s += "<div class='men-thumb-item'>";
                s += "<div><img class='img-responsive' src='../static/media/" + ar[i]['photo'] + "' style='width: 600px; height: 200px'></div>";
                s += "<div class='men-cart-pro'>";
                s += "<div class='inner-men-cart-pro'>";
                s += "<button style='border: 0px; border-radius: 20px' class='link-product-add-cart' onclick='quickview(" + ar[i]['pid'] + ")'>Quick View</button>";
                s += "</div>";
                s += "</div>";
                s += "<span class='product-new-top'>New</span>";
                s += "</div>";
                s += "<div class='item-info-product'>";
                s += "<div class='info-product-price'>";
                s += "<div class='grid_meta'>";
                s += "<div class='product_price'>";
                s += "<h4 class='text-center'>" + ar[i]['pname'] + "</h4>";
                s += "<div class='grid-price mt-2'>";
                s += "<div class='text-center'><span class='money' style='color: blue;'>₹ " + ar[i]['price'] + "</span><del style='color: red;'>₹ " + ar[i]['mrp'] + "</del></div>";
                s += "</div>";
                s += "</div>";
                s += "</div>";
                s += "</div>";
                s += "<div class='toys single-item hvr-outline-out'>";
                s += "<button type='button' class='toys-cart ptoys-cart btn btn-success' style='margin-top: -10px' onclick='addtocart(" + ar[i]['pid'] + "," + ar[i]['price'] + ")'><i class='fas fa-cart-plus'></i></button>";
                s += "</div>";
                s += "</div>";
                s += "</div>";
                s += "</div>";
                s += "</div>";
            }
            document.getElementById('output').innerHTML = s;
        }
    };
    xml.open('POST', 'showcat', true);
    xml.send(formdata);
}

function showreviews(pid) {
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var ar = JSON.parse(this.response);
            if(ar != "") {
                var s = "";
                s += "<section class='py-lg-4 py-md-3 py-sm-3 py-3' style='background: url(../static/images/pic23.png)'>";
                s += "<div class='container py-lg-5 py-md-5 py-sm-4 py-3'>";
                s += "<h3 class='title clr text-center mb-lg-5 mb-md-4 mb-sm-4 mb-3'>Customers Review</h3>";
                s += "<div id='carouselExampleControls' class='carousel slide' data-ride='carousel'>";
                s += "<div class='carousel-inner'>";
                for (var i = 0; i < ar.length; i++) {
                    s += "<div style='background-color: whitesmoke; border-radius: 30px'>";
                    s += "<br>";
                    s += "<table style='margin-left: 20px;'>";
                    s += "<tr>";
                    s += "<td style=' font-size: 18px'>" + ar[i]['email'] + "<br><br></td>";
                    s += "</tr>";
                    s += "<tr>";
                    s += "<td>" + ar[i]['content'] + "</td>";
                    s += "</tr>";
                    s += "</table>";
                    s += "<br>";
                    s += "</div>";
                    s += "<br><br>";
                }
                s += "</div>";
                s += "</div>";
                s += "</div>";
                s += "</section>";
                document.getElementById('output_review').innerHTML = s;
            }
        }
    };
    xml.open('GET', 'showreviewsaction?pid='+pid, true);
    xml.send();
}