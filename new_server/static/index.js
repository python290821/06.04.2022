var x = {}

function add_customer() {
    console.log('==========================')
    //$.ajax({url:"/customers"})
    customer = {
        id: parseInt($('#txt_id').val()),
        name: $('#txt_name').val(),
        address: $('#txt_address').val(),
        email: $('#txt_email').val()
    }
    console.log(customer)
    $.ajax({
            type: "POST",
            url: "/customers",
            data: JSON.stringify(customer),
            dataType: "JSON",
            contentType: 'application/json',
            success: function(data, status){
                console.log('status', status)
                console.log('data', data)
                get_all_customers(true)
            },
            error: function (xhr, desc, err) {
            }
            });

}
function get_customer_by_id() {
     $.ajax({url:"/customers/" + $('#txt_id_u').val()}).then(
      function(one_customer) // after-promise succeed
                {
                    console.log(one_customer)
                    $('#txt_name_u').val(one_customer.name)
                    $('#txt_email_u').val(one_customer.email)
                    $('#txt_address_u').val(one_customer.address)
                });
}

function update_customer(customer) {
    // homework
}

function delete_customer(id) {
    console.log(`send ajax to delete where customer id = ${id}`)

    // delete the customer
    $.ajax({
            type: "DELETE",
            url: "/customers/" + id,
            success: function(data, status){
                console.log('status', status)
                console.log('data', data)
                get_all_customers(false)
            },
            error: function (xhr, desc, err) {
            }
            });
}

function get_all_customers(draw_last_only) {
        var customers_table =  $("#customers"); //cache

        if (!draw_last_only)
            customers_table.find("tr:gt(0)").remove();

        $.ajax({url:"/customers"}).then(
                function(_customers) // after-promise succeed
                {
                x.result = _customers
                    console.log(_customers);
                    console.log(_customers[0])

                   $.each(_customers,  (i, customer) => {
                            if (!draw_last_only || i == _customers.length - 1) {
                                customers_table.append(
                                    `<tr><td>${customer.id}</td>
                                         <td>${customer.name}</td>
                                         <td>${customer.address}</td>
                                         <td>${customer.email}</td>
                                         <td><button style="color:red" onclick="delete_customer(${customer.id})">X</button></td></tr>`)
                                         };
                    })
                }
                ,function(err)   // after-promise failed
                {
                    console.log(err);}
                );
}

$(document).ready(function()
{
    $('#btn1').on('click', () => {

        get_all_customers(false);

    });
});