#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>

using namespace std::chrono_literals;

class SimpleDriverNode : public rclcpp::Node {
public:
    SimpleDriverNode() : Node("simple_driver") {
        // Publish to the exact topic the Diff Drive plugin is listening to
        publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/cmd_vel", 10);
        
        // Run the timer 20 times a second (50ms)
        timer_ = this->create_wall_timer(50ms, std::bind(&SimpleDriverNode::timer_callback, this));
        
        RCLCPP_INFO(this->get_logger(), "Driver Node started! Driving in a circle...");
    }

private:
    void timer_callback() {
        auto message = geometry_msgs::msg::Twist();
        message.linear.x = 0.2;  // Move forward at 0.2 m/s
        message.angular.z = 0.5; // Turn left at 0.5 rad/s
        publisher_->publish(message);
    }

    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<SimpleDriverNode>());
    rclcpp::shutdown();
    return 0;
}