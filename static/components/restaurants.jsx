var Restaurants = React.createClass({

    getInitialState: function(){
      return{
        activePage: 1,
        data: []
      }
    },

    componentDidMount: function() {
        this.loadRestaurants();
    },

    loadRestaurants: function(){
      $.ajax({
        method: 'GET',
        url: '/get_restaurants',
        data:{
          page: this.state.activePage,
          per: 10
        },
        success: (response) => {
          console.log(JSON.parse(response));
          this.setState({
            data: JSON.parse(response)
          });
        }
      })
    },

    handlePageChange: function(ev){
      console.log("Changed page: ", ev.target);
    },

    render: function() {
        return (
            <div className="container restaurant-wrapper">
                <div className="row">

                    {this.state.data.map(function(item){
                      return <RestaurantItem data={item} key={item._id.$oid} />
                    })}

                </div>
            </div>
        );
    }
});

var RestaurantItem = React.createClass({
  render: function(){
    return(
      <div className="col-sm-6">
          <div className="panel panel-primary">
              <div className="panel-heading">Example panel</div>
              <div className="panel-body"></div>
              <div className="panel-footer">Example footer</div>
          </div>
      </div>
    )
  }
});

ReactDOM.render(React.createElement(Restaurants, null), document.getElementById('restaurants'));
